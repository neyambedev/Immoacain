document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const container = document.getElementById("terrain-container");

    // Vérification que les éléments sont bien trouvés
    if (!input) {
        console.error("Élément search-input introuvable!");
        return;
    }
    if (!container) {
        console.error("Élément terrain-container introuvable!");
        return;
    }

    console.log("Script de filtrage chargé avec succès");

    // Fonction de recherche
    const rechercherTerrains = () => {
        const quartier = input.value.trim();
        console.log("Recherche pour:", quartier);

        fetch(`/filtrer_terrains?q=${encodeURIComponent(quartier)}`)
            .then(response => {
                console.log("Réponse reçue:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Données reçues:", data.terrains.length, "terrains");
                
                // Structure complète avec la div "cont" et "terrains"
                let htmlContent = `
                <div class="cont">
                    <div class="terrains">
                        <div class="h2">
                            <h2 class="text-center mb-5">Liste des terrains disponibles</h2>
                        </div>
                        <div class="row g-4">
                `;

                if (data.terrains.length === 0) {
                    htmlContent += `
                        <p class="text-center">Aucun terrain trouvé.</p>
                    `;
                } else {
                    data.terrains.forEach(terrain => {
                        let imagesHtml = "";
                        let carouselHtml = "";

                        // Génération du carrousel seulement si des images existent
                        if (terrain.images && terrain.images.length > 0) {
                            terrain.images.forEach((img, index) => {
                                imagesHtml += `
                                    <div class="carousel-item ${index === 0 ? "active" : ""}">
                                        <img src="${img}" class="im d-block" alt="Image terrain ${terrain.titre}">
                                    </div>
                                `;
                            });

                            carouselHtml = `
                                <div id="carouselTerrain${terrain.id}" class="carousel slide" data-bs-ride="false">
                                    <div class="carousel-inner w-100">
                                        ${imagesHtml}
                                    </div>
                                    <button class="carousel-control-prev" type="button" data-bs-target="#carouselTerrain${terrain.id}" data-bs-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Précédent</span>
                                    </button>
                                    <button class="carousel-control-next" type="button" data-bs-target="#carouselTerrain${terrain.id}" data-bs-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Suivant</span>
                                    </button>
                                </div>
                            `;
                        }

                        htmlContent += `
                            <div class="col-12 col-md-6 col-lg-4">
                                <div class="card terrain-card h-100">
                                    ${carouselHtml}
                                    <div class="card-body">
                                        <h5 class="card-title text-center text-primary">${terrain.titre}</h5>
                                        <p><strong>Id:</strong> ${terrain.id}</p>
                                        <p><strong>Proprietaire :</strong> ${terrain.proprietaire}</p>
                                        <p><strong>Superficie :</strong> ${terrain.superficie} <strong>m²</strong></p>
                                        <p><strong>Prix :</strong> ${terrain.prix} <strong>Fcfa</strong></p>
                                        <p><strong>Ville:</strong> ${terrain.localisation} </p>
                                        <p><strong>Quartier:</strong> ${terrain.quartier} </p>
                                        <p><strong>Description :</strong> ${terrain.description}</p>
                                        
                                    </div>
                                    <div class="card-footer text-muted text-center">
                                        Ajouté le ${terrain.date_ajout}
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                }

                htmlContent += `
                        </div>
                    </div>
                </div>
                `;

                container.innerHTML = htmlContent;
                console.log("Contenu mis à jour");
            })
            .catch(error => {
                console.error("Erreur lors de la recherche:", error);
            });
    };

    // Événement sur chaque frappe clavier
    input.addEventListener("keyup", rechercherTerrains);
    
    // Événement sur le changement de valeur
    input.addEventListener("input", rechercherTerrains);
});




