/**
 * Filtrage du catalogue des API.
 *
 * Les tuiles portent leurs métadonnées en attributs `data-*`, générés par le
 * hook MkDocs à partir des en-têtes YAML des fiches. Le filtrage est donc
 * intégralement côté client, sans appel réseau, et le site reste utilisable
 * sans JavaScript : toutes les tuiles sont alors affichées.
 */
(function () {
  'use strict';

  var GROUPES = ['theme', 'acces', 'statut'];
  var PARAM_RECHERCHE = 'q';

  function initialiser() {
    var grille = document.getElementById('catalogue-grille');
    if (!grille) {
      return;
    }

    var items = Array.prototype.slice.call(grille.querySelectorAll('.catalogue__item'));
    var cases = Array.prototype.slice.call(document.querySelectorAll('[data-filtre]'));
    var recherche = document.getElementById('catalogue-recherche');
    var boutonRecherche = document.getElementById('catalogue-recherche-btn');
    var reinitialiser = document.getElementById('catalogue-reinitialiser');
    var resultats = document.getElementById('catalogue-resultats');
    var vide = document.getElementById('catalogue-vide');
    var actifs = document.getElementById('catalogue-actifs');
    var total = items.length;

    /** Retourne les valeurs cochées, par groupe de filtre. */
    function selection() {
      var etat = {};
      GROUPES.forEach(function (groupe) {
        etat[groupe] = cases
          .filter(function (c) {
            return c.dataset.filtre === groupe && c.checked;
          })
          .map(function (c) {
            return c.value;
          });
      });
      return etat;
    }

    function normaliser(texte) {
      return texte
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .trim();
    }

    /** Reconstruit la liste des filtres actifs, chacun retirable au clic. */
    function afficherFiltresActifs(etat) {
      actifs.innerHTML = '';
      cases
        .filter(function (c) {
          return c.checked;
        })
        .forEach(function (c) {
          var label = document.querySelector('label[for="' + c.id + '"]');
          var texte = label
            ? label.textContent.replace(/\s*\d+\s*$/, '').trim()
            : c.value;
          var bouton = document.createElement('button');
          bouton.type = 'button';
          bouton.className = 'catalogue__actif';
          bouton.innerHTML =
            texte + ' <span aria-hidden="true">&times;</span>';
          bouton.setAttribute('aria-label', 'Retirer le filtre ' + texte);
          bouton.addEventListener('click', function () {
            c.checked = false;
            appliquer();
          });
          actifs.appendChild(bouton);
        });
      void etat;
    }

    function appliquer() {
      var etat = selection();
      var terme = normaliser(recherche ? recherche.value : '');
      var visibles = 0;

      items.forEach(function (item) {
        var correspond = GROUPES.every(function (groupe) {
          var valeurs = etat[groupe];
          return valeurs.length === 0 || valeurs.indexOf(item.dataset[groupe]) !== -1;
        });

        if (correspond && terme) {
          correspond = normaliser(item.dataset.recherche || '').indexOf(terme) !== -1;
        }

        item.hidden = !correspond;
        if (correspond) {
          visibles += 1;
        }
      });

      if (resultats) {
        resultats.textContent =
          visibles === total
            ? total + ' API sur ' + total
            : visibles + ' API sur ' + total + ' après filtrage';
      }
      if (vide) {
        vide.hidden = visibles !== 0;
      }
      afficherFiltresActifs(etat);
      memoriser(etat, recherche ? recherche.value : '');
    }

    /** Reflète l'état des filtres dans l'URL : les vues sont partageables. */
    function memoriser(etat, terme) {
      if (!window.history || !window.history.replaceState) {
        return;
      }
      var params = new URLSearchParams();
      GROUPES.forEach(function (groupe) {
        etat[groupe].forEach(function (valeur) {
          params.append(groupe, valeur);
        });
      });
      if (terme) {
        params.set(PARAM_RECHERCHE, terme);
      }
      var suffixe = params.toString();
      window.history.replaceState(
        null,
        '',
        window.location.pathname + (suffixe ? '?' + suffixe : '')
      );
    }

    /** Restaure les filtres transmis dans l'URL. */
    function restaurer() {
      var params = new URLSearchParams(window.location.search);
      GROUPES.forEach(function (groupe) {
        var valeurs = params.getAll(groupe);
        cases.forEach(function (c) {
          if (c.dataset.filtre === groupe && valeurs.indexOf(c.value) !== -1) {
            c.checked = true;
          }
        });
      });
      if (recherche && params.get(PARAM_RECHERCHE)) {
        recherche.value = params.get(PARAM_RECHERCHE);
      }
    }

    cases.forEach(function (c) {
      c.addEventListener('change', appliquer);
    });

    if (recherche) {
      var minuteur;
      recherche.addEventListener('input', function () {
        window.clearTimeout(minuteur);
        minuteur = window.setTimeout(appliquer, 200);
      });
      recherche.addEventListener('keydown', function (evenement) {
        if (evenement.key === 'Enter') {
          evenement.preventDefault();
          appliquer();
        }
      });
    }

    if (boutonRecherche) {
      boutonRecherche.addEventListener('click', appliquer);
    }

    if (reinitialiser) {
      reinitialiser.addEventListener('click', function () {
        cases.forEach(function (c) {
          c.checked = false;
        });
        if (recherche) {
          recherche.value = '';
        }
        appliquer();
        if (recherche) {
          recherche.focus();
        }
      });
    }

    restaurer();
    appliquer();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialiser);
  } else {
    initialiser();
  }
})();
