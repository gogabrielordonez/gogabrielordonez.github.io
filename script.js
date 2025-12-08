// Basic script for interaction
document.addEventListener('DOMContentLoaded', () => {
    console.log("Portfolio loaded.");

    // Mobile Navigation
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');
    const navLinks = document.querySelectorAll('.nav-link');

    function openMenu() {
        navMenu.classList.add('active');
        navOverlay.classList.add('active');
        document.body.classList.add('menu-open');
        navToggle.innerHTML = "<i class='bx bx-x'></i>";
    }

    function closeMenu() {
        navMenu.classList.remove('active');
        navOverlay.classList.remove('active');
        document.body.classList.remove('menu-open');
        navToggle.innerHTML = "<i class='bx bx-menu'></i>";
    }

    navToggle.addEventListener('click', () => {
        if (navMenu.classList.contains('active')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    navOverlay.addEventListener('click', closeMenu);

    // Close menu when clicking a nav link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            closeMenu();
        });
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            e.preventDefault();
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.padding = '1rem 0';
            navbar.style.background = 'rgba(10, 10, 15, 0.95)';
        } else {
            navbar.style.padding = '1.5rem 0';
            navbar.style.background = 'rgba(10, 10, 15, 0.8)';
        }
    });

    // Fetch GitHub repositories
    fetchGitHubRepos();
});

// GitHub API integration
const GITHUB_USERNAME = 'gogabrielordonez';

async function fetchGitHubRepos() {
    const container = document.getElementById('repos-container');

    try {
        const response = await fetch(
            `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=12`
        );

        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }

        const repos = await response.json();

        // Filter out forked repos and sort by stars, then by update date
        const filteredRepos = repos
            .filter(repo => !repo.fork)
            .sort((a, b) => b.stargazers_count - a.stargazers_count ||
                           new Date(b.updated_at) - new Date(a.updated_at));

        if (filteredRepos.length === 0) {
            container.innerHTML = `
                <div class="repos-loading">
                    <p>No public repositories found.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = filteredRepos.map(repo => createRepoCard(repo)).join('');

    } catch (error) {
        console.error('Error fetching GitHub repos:', error);
        container.innerHTML = `
            <div class="repos-error">
                <i class='bx bx-error-circle' style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                <p>Unable to load repositories. Please visit my
                   <a href="https://github.com/${GITHUB_USERNAME}" target="_blank" style="color: var(--accent);">GitHub profile</a> directly.
                </p>
            </div>
        `;
    }
}

function createRepoCard(repo) {
    const languageClass = repo.language ? `lang-${repo.language.toLowerCase()}` : '';
    const description = repo.description || 'No description available';
    const updatedDate = new Date(repo.updated_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short'
    });

    return `
        <div class="repo-card fade-in">
            <h3>
                <i class='bx bx-git-repo-forked' style="color: var(--text-secondary);"></i>
                <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer">${repo.name}</a>
            </h3>
            <p class="repo-description">${description}</p>
            <div class="repo-meta">
                ${repo.language ? `<span class="repo-language ${languageClass}">${repo.language}</span>` : ''}
                <span><i class='bx bx-star'></i> ${repo.stargazers_count}</span>
                <span><i class='bx bx-git-branch'></i> ${repo.forks_count}</span>
                <span><i class='bx bx-time-five'></i> ${updatedDate}</span>
            </div>
        </div>
    `;
}
