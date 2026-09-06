/**
 * Affichage des spécifications OpenAPI avec Redoc.
 *
 * Le bundle est d'abord cherché dans `assets/javascripts/vendor/` afin que le
 * site fonctionne sans accès Internet (réseau interministériel, poste hors
 * ligne, recette). En son absence, le CDN sert de repli.
 *
 * La spécification affichée peut provenir de deux sources, déclarées dans
 * l'en-tête YAML de la fiche :
 *   - `openapi` : un fichier hébergé par ce site ;
 *   - `openapi_url` : l'URL publiée par le producteur de l'API.
 * Quand les deux existent, la fiche propose un sélecteur de source.
 *
 * Le rendu n'est pas déclenché au chargement de la page : Redoc pèse près d'un
 * mégaoctet et la plupart des visiteurs lisent d'abord la description
 * fonctionnelle. Un bouton explicite déclenche le chargement, ce qui évite
 * aussi une requête réseau non sollicitée vers la spécification distante.
 */
(function () {
  'use strict';

  var chargement = null;

  function chargerScript(url) {
    return new Promise(function (resoudre, rejeter) {
      var script = document.createElement('script');
      script.src = url;
      script.async = true;
      script.onload = function () {
        resoudre();
      };
      script.onerror = function () {
        rejeter(new Error('Chargement impossible : ' + url));
      };
      document.head.appendChild(script);
    });
  }

  function chargerRedoc(local, cdn) {
    if (window.Redoc) {
      return Promise.resolve();
    }
    if (!chargement) {
      chargement = chargerScript(local).catch(function () {
        return chargerScript(cdn);
      });
    }
    return chargement;
  }

  function options() {
    return {
      scrollYOffset: 0,
      hideDownloadButton: true,
      nativeScrollbars: true,
      expandResponses: '200,201',
      jsonSampleExpandLevel: 2,
      theme: {
        colors: { primary: { main: '#000091' } },
        typography: {
          fontFamily: '"Marianne", arial, sans-serif',
          headings: { fontFamily: '"Marianne", arial, sans-serif' }
        },
        sidebar: { width: '260px' }
      }
    };
  }

  function messageAttente(cible) {
    cible.innerHTML =
      '<p class="fr-p-3w fr-text--sm">Chargement de la documentation…</p>';
  }

  function messageErreur(cible, url) {
    var lien = document.createElement('a');
    lien.className = 'fr-link';
    lien.href = url;
    lien.textContent = url;

    cible.innerHTML =
      '<div class="fr-alert fr-alert--warning redoc__erreur">' +
      '<h3 class="fr-alert__title">Documentation indisponible</h3>' +
      '<p>Le rendu interactif n\'a pas pu être chargé. La spécification reste ' +
      'consultable et téléchargeable à l\'adresse ci-dessous.</p></div>';
    cible.querySelector('.redoc__erreur').appendChild(lien);
  }

  function afficher(bloc, cible, bouton) {
    var specification = bloc.dataset.redocSpec;

    cible.setAttribute('aria-busy', 'true');
    messageAttente(cible);
    if (bouton) {
      bouton.disabled = true;
    }

    chargerRedoc(bloc.dataset.redocBundle, bloc.dataset.redocCdn)
      .then(function () {
        window.Redoc.init(specification, options(), cible, function (erreur) {
          cible.removeAttribute('aria-busy');
          if (bouton) {
            bouton.disabled = false;
            bouton.textContent = 'Recharger la documentation';
          }
          if (erreur) {
            messageErreur(cible, specification);
          }
        });
      })
      .catch(function () {
        cible.removeAttribute('aria-busy');
        if (bouton) {
          bouton.disabled = false;
        }
        messageErreur(cible, specification);
      });
  }

  function initialiser() {
    var blocs = document.querySelectorAll('.redoc[data-redoc-spec]');

    Array.prototype.forEach.call(blocs, function (bloc) {
      var cible = bloc.querySelector('[data-redoc-cible]');
      var bouton = bloc.querySelector('[data-redoc-afficher]');
      var sources = bloc.querySelectorAll('[data-redoc-source]');

      if (!cible) {
        return;
      }

      if (bouton) {
        bouton.addEventListener('click', function () {
          afficher(bloc, cible, bouton);
        });
      }

      Array.prototype.forEach.call(sources, function (source) {
        source.addEventListener('change', function () {
          if (!source.checked) {
            return;
          }
          bloc.dataset.redocSpec = source.value;
          // On ne relance le rendu que si la documentation est déjà affichée.
          if (cible.childElementCount && !cible.querySelector('noscript')) {
            afficher(bloc, cible, bouton);
          }
        });
      });

      // Une ancre pointant vers un chemin d'API ouvre directement la
      // documentation : c'est le seul cas où le rendu est automatique.
      if (window.location.hash.indexOf('#operation') === 0 && bouton) {
        afficher(bloc, cible, bouton);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialiser);
  } else {
    initialiser();
  }
})();
