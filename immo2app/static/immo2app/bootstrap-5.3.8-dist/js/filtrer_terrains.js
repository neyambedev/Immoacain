document.addEventListener("DOMContentLoaded", () => {
    const input     = document.getElementById("search-input");
    const container = document.getElementById("terrain-container");

    if (!input || !container) return;

    // ── Génère le badge type ────────────────────────────────
    function badgeType(type) {
        const map = {
            terrain:  { icon: 'bi-geo-alt-fill',  label: 'Terrain'  },
            maison:   { icon: 'bi-house-fill',     label: 'Maison'   },
            location: { icon: 'bi-key-fill',       label: 'Location' },
        };
        const t = map[type] || { icon: 'bi-building', label: type };
        return `<span class="badge-type badge-${type}">
                    <i class="bi ${t.icon}"></i> ${t.label}
                </span>`;
    }

    // ── Génère le carousel ou le placeholder ───────────────
    function carouselHtml(terrain) {
        if (!terrain.images || terrain.images.length === 0) {
            return `<div class="carousel-inner-placeholder">
                        <i class="bi bi-image"></i>
                    </div>`;
        }

        const items = terrain.images.map((img, i) => `
            <div class="carousel-item ${i === 0 ? 'active' : ''}">
                <img src="${img}" alt="${terrain.titre}">
            </div>`).join('');

        const controls = terrain.images.length > 1 ? `
            <button class="carousel-control-prev" type="button"
                data-bs-target="#carousel${terrain.id}" data-bs-slide="prev">
                <span class="carousel-control-prev-icon"></span>
            </button>
            <button class="carousel-control-next" type="button"
                data-bs-target="#carousel${terrain.id}" data-bs-slide="next">
                <span class="carousel-control-next-icon"></span>
            </button>` : '';

        return `<div id="carousel${terrain.id}" class="carousel slide" data-bs-ride="false">
                    <div class="carousel-inner">${items}</div>
                    ${controls}
                </div>`;
    }

    // ── Génère une carte complète ───────────────────────────
    function carteHtml(terrain) {
        const prixSuffix = terrain.type_bien === 'location'
            ? (terrain.categorie_location === 'hotel' || terrain.categorie_location === 'Hôtel'
                ? `<span class="prix-mois"> / heure</span>`
                : `<span class="prix-mois"> / mois</span>`)
            : '';

        return `
        <div class="col-12 col-md-6 col-lg-4">
            <div class="terrain-card card-${terrain.type_bien} fade-in">

                ${badgeType(terrain.type_bien)}
                ${carouselHtml(terrain)}

                <div class="card-body">
                    <h5 class="card-title">${terrain.titre}</h5>

                    <div class="prix-badge">
                        <i class="bi bi-cash-coin"></i>
                        ${terrain.prix}${prixSuffix}
                    </div>

                    <div class="bien-details">
                        <div class="detail-item">
                            <i class="bi bi-person-circle text-primary"></i>
                            <div><strong>Propriétaire</strong><span>${terrain.proprietaire}</span></div>
                        </div>
                        ${terrain.type_bien === 'location' ? `
                        <div class="detail-item">
                            <i class="bi bi-tag-fill text-primary"></i>
                            <div><strong>Catégorie</strong><span>${terrain.categorie_location || '—'}</span></div>
                        </div>
                        <div class="detail-item">
                            <i class="bi bi-signpost-fill text-primary"></i>
                            <div><strong>Nom</strong><span>${terrain.nom_location || '—'}</span></div>
                        </div>
                        ` : `
                        <div class="detail-item">
                            <i class="bi bi-rulers text-primary"></i>
                            <div><strong>Surface</strong><span>${terrain.superficie} m²</span></div>
                        </div>
                        `}
                        <div class="detail-item">
                            <i class="bi bi-building text-primary"></i>
                            <div><strong>Ville</strong><span>${terrain.localisation}</span></div>
                        </div>
                        <div class="detail-item">
                            <i class="bi bi-geo-alt-fill text-danger"></i>
                            <div><strong>Quartier</strong><span>${terrain.quartier}</span></div>
                        </div>
                    </div>

                    <p class="card-description">${terrain.description}</p>
                </div>

                <div class="card-footer">
                    <i class="bi bi-calendar3"></i> ${terrain.date_ajout}
                </div>

            </div>
        </div>`;
    }

    // ── Requête de recherche ────────────────────────────────
    let timer = null;

    const rechercher = () => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            const q = input.value.trim();

            fetch(`/filtrer_terrains?q=${encodeURIComponent(q)}`)
                .then(r => r.json())
                .then(data => {
                    const terrains = data.terrains;

                    let html = `
                    <div class="container-modern">
                        <h1 class="section-title fade-in">
                            <i class="bi bi-buildings"></i>
                            ${q ? `Résultats pour "<em>${q}</em>"` : 'Biens disponibles'}
                        </h1>
                        <div class="row g-4">`;

                    if (terrains.length === 0) {
                        html += `<div class="col-12">
                                    <div class="empty-state">
                                        <i class="bi bi-search"></i>
                                        <p>Aucun bien ne correspond à votre recherche.</p>
                                    </div>
                                 </div>`;
                    } else {
                        terrains.forEach(t => { html += carteHtml(t); });
                    }

                    html += `</div></div>`;
                    container.innerHTML = html;
                })
                .catch(err => console.error("Erreur filtrage:", err));
        }, 300); // délai 300ms après la dernière frappe
    };

    input.addEventListener("input", rechercher);
});
