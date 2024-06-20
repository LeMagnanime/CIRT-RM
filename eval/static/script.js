let places = [];
let transitions = [];
let arcs = [];
let placeCounter = 1;
let transitionCounter = 1;
let selectedElement = null;
let running = false;
let simulationInterval;
let drawingArc = false;

function addPlace() {
    const place = document.createElement('div');
    place.className = 'place';
    place.id = `P${placeCounter++}`;
    place.style.left = `${Math.random() * 80}%`;
    place.style.top = `${Math.random() * 80}%`;
    place.innerHTML = `<div class="tokens"></div>${place.id}`;
    document.getElementById('petri-net').appendChild(place);
    places.push(place);
    makeDraggable(place);
}

function addTransition() {
    const transition = document.createElement('div');
    transition.className = 'transition';
    transition.id = `T${transitionCounter++}`;
    transition.style.left = `${Math.random() * 80}%`;
    transition.style.top = `${Math.random() * 80}%`;
    transition.innerHTML = transition.id;
    document.getElementById('petri-net').appendChild(transition);
    transitions.push(transition);
    makeDraggable(transition);
}

function makeDraggable(element) {
    interact(element).draggable({
        listeners: {
            move(event) {
                const target = event.target;
                const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

                target.style.transform = `translate(${x}px, ${y}px)`;

                target.setAttribute('data-x', x);
                target.setAttribute('data-y', y);

                updateArcs();
            }
        }
    });
}

function updateArcs() {
    arcs.forEach(arc => {
        const start = document.getElementById(arc.start);
        const end = document.getElementById(arc.end);
        const line = document.getElementById(arc.id);

        const startRect = start.getBoundingClientRect();
        const endRect = end.getBoundingClientRect();
        const containerRect = document.getElementById('petri-net').getBoundingClientRect();

        line.setAttribute('x1', startRect.left + startRect.width / 2 - containerRect.left);
        line.setAttribute('y1', startRect.top + startRect.height / 2 - containerRect.top);
        line.setAttribute('x2', endRect.left + endRect.width / 2 - containerRect.left);
        line.setAttribute('y2', endRect.top + endRect.height / 2 - containerRect.top);
    });
}

function addArc(startId, endId) {
    const arcId = `A${arcs.length + 1}`;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.className = 'arc';
    line.id = arcId;
    line.setAttribute('stroke', 'black');
    line.setAttribute('stroke-width', '2');
    document.getElementById('svg-canvas').appendChild(line);

    arcs.push({ id: arcId, start: startId, end: endId });
    updateArcs();
}

document.getElementById('petri-net').addEventListener('click', event => {
    const target = event.target;
    if (target.classList.contains('place') || target.classList.contains('transition')) {
        if (drawingArc) {
            if (selectedElement && selectedElement !== target) {
                addArc(selectedElement.id, target.id);
                selectedElement.style.border = 'none'; // Remove highlight from previously selected element
                selectedElement = null;
                drawingArc = false;
            }
        } else {
            if (selectedElement) {
                selectedElement.style.border = 'none'; // Remove highlight from previously selected element
            }
            selectedElement = target;
            target.style.border = '2px solid red'; // Highlight selected element
            drawingArc = true;
        }
    }
});

function removeElement() {
    if (selectedElement) {
        // Remove all associated arcs
        arcs = arcs.filter(arc => {
            if (arc.start === selectedElement.id || arc.end === selectedElement.id) {
                const line = document.getElementById(arc.id);
                line.parentNode.removeChild(line);
                return false;
            }
            return true;
        });

        // Remove the element itself
        selectedElement.parentNode.removeChild(selectedElement);
        selectedElement = null;
        drawingArc = false;
    }
}

function clearNet() {
    document.getElementById('petri-net').innerHTML = '<svg id="svg-canvas" style="position:absolute; width:100%; height:100%; pointer-events:none;"></svg>';
    places = [];
    transitions = [];
    arcs = [];
    placeCounter = 1;
    transitionCounter = 1;
    selectedElement = null;
    stopNet(); // Stop the simulation if it's running
}

function runNet() {
    createTokenInFirstPlace();
    running = true;
    moveTokenThroughNet('P1'); // Démarrer le mouvement du token à partir de la première place
}

function stopNet() {
    if (running) {
        clearInterval(simulationInterval);
        running = false;
    }
}

function enableLinkMode() {
    drawingArc = true;
    if (selectedElement) {
        selectedElement.style.border = 'none';
        selectedElement = null;
    }
}

// Fonction pour créer un token dans la première place
function createTokenInFirstPlace() {
    const firstPlace = places[0];
    const token = document.createElement('div');
    token.className = 'token';
    token.style.display = 'block';
    firstPlace.querySelector('.tokens').appendChild(token);
}

// Fonction pour animer le déplacement du token entre deux éléments
function animateToken(token, startElement, endElement, duration, callback) {
    const startPosition = {
        x: startElement.offsetLeft + startElement.offsetWidth / 2,
        y: startElement.offsetTop + startElement.offsetHeight / 2
    };

    const endPosition = {
        x: endElement.offsetLeft + endElement.offsetWidth / 2,
        y: endElement.offsetTop + endElement.offsetHeight / 2
    };

    const distanceX = endPosition.x - startPosition.x;
    const distanceY = endPosition.y - startPosition.y;

    let startTime;

    function moveToken(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);

        token.style.left = startPosition.x + distanceX * progress + 'px';
        token.style.top = startPosition.y + distanceY * progress + 'px';

        if (progress < 1) {
            requestAnimationFrame(moveToken);
        } else {
            token.style.left = endPosition.x + 'px';
            token.style.top = endPosition.y + 'px';
            if (callback) callback();
        }
    }

    requestAnimationFrame(moveToken);
}

// Fonction pour déplacer le token à travers le réseau de Petri
function moveTokenThroughNet(currentPlaceId) {
    const token = document.querySelector('.token');
    const currentPlace = document.getElementById(currentPlaceId);
    const outgoingArcs = arcs.filter(arc => arc.start === currentPlaceId);

    if (outgoingArcs.length > 0) {
        const nextArc = outgoingArcs[0]; // Prenons le premier arc sortant pour l'exemple
        const nextElement = document.getElementById(nextArc.end);

        animateToken(token, currentPlace, nextElement, 1000, () => {
            if (nextElement.classList.contains('transition')) {
                const nextPlaceArcs = arcs.filter(arc => arc.start === nextElement.id);
                if (nextPlaceArcs.length > 0) {
                    const nextPlace = nextPlaceArcs[0].end;
                    moveTokenThroughNet(nextPlace);
                }
            }
        });
    }
}
// Fonction pour récupérer les informations des places et transitions
function getPlacesAndTransitionsInfo() {
    const placesInfo = places.map(place => ({
        id: place.id,
        // Autres informations pertinentes à ajouter
    }));

    const transitionsInfo = transitions.map(transition => ({
        id: transition.id,
        // Autres informations pertinentes à ajouter
    }));

    return { places: placesInfo, transitions: transitionsInfo };
}

// Fonction pour afficher les informations des places et transitions dans une fenêtre modale
// Définition de la fonction showAutomataDefinition en dehors de l'événement DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Votre code ici
    const modal = document.getElementById('myModal');
    const btnOpen = document.getElementById('openModal');
    const spanClose = document.getElementsByClassName('close')[0];

    btnOpen.onclick = function() {
        modal.style.display = "block";
    }

    spanClose.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
});
function showPopup() {
    const placesAndTransitionsInfo = getPlacesAndTransitionsInfo(); // Appel de votre fonction pour obtenir les informations

    // Génération du contenu HTML pour le popup
    let popupContent = '<div>';
    placesAndTransitionsInfo.places.forEach(place => {
        popupContent += `${place.id}`;
        // Ajouter d'autres informations si nécessaire
    });
    placesAndTransitionsInfo.transitions.forEach(transition => {
        popupContent += `${transition.id}`;
        // Ajouter d'autres informations si nécessaire
    });
    popupContent += '</div>';

    // Affichage du popup avec les informations
    alert(popupContent); // Vous pouvez aussi utiliser une boîte de dialogue plus élaborée
}
function clearNuSMVCode() {
    document.getElementById("nusmv_code").value = ""; // Efface le contenu du champ de texte
}
