const menu = document.getElementById('menu');
const indicador = document.getElementById('indicador');
const secciones = document.querySelectorAll('.seccion');

let tamañoIndicador = menu.querySelector('a').offsetWidth;
indicador.style.width = tamañoIndicador + 'px';

let indexSeccionActiva;

// Observer
const observer = new IntersectionObserver((entradas, observer) => {
	entradas.forEach(entrada => {
		if(entrada.isIntersecting){
			// Obtenemos cual es la seccion que esta entrando en pantalla.
			// console.log(`La entrada ${entrada.target.id} esta intersectando`);

			// Creamos un arreglo con las secciones y luego obtenemos el index del la seccion que esta en pantalla.
			indexSeccionActiva = [...secciones].indexOf(entrada.target);
			indicador.style.transform = `translateX(${tamañoIndicador * indexSeccionActiva}px)`;
		}
	});
}, {
	rootMargin: '-80px 0px 0px 0px',
	threshold: 0.2
});

// Agregamos un observador para el hero.
observer.observe(document.getElementById('hero'));

// Asignamos un observador a cada una de las secciones
secciones.forEach(seccion => observer.observe(seccion));

// Evento para cuando la pantalla cambie de tamaño.
const onResize = () => {
	// Calculamos el nuevo tamaño que deberia tener el indicador.
	tamañoIndicador = menu.querySelector('a').offsetWidth;

	// Cambiamos el tamaño del indicador.
	indicador.style.width = `${tamañoIndicador}px`;

	// Volvemos a posicionar el indicador.
	indicador.style.transform = `translateX(${tamañoIndicador * indexSeccionActiva}px)`;
}

window.addEventListener('resize', onResize);


/* TAGS

const tagInput = document.getElementById("tagInput");
const tagList = document.getElementById("tagList");

document.getElementById("addTagButton").addEventListener("click", function() {
  const newTag = tagInput.value;
  if (newTag !== "") {
    const tagListItem = document.createElement("li");
    tagListItem.innerText = newTag;
    tagList.appendChild(tagListItem);
    tagInput.value = "";
  }
});
*/

const tagInput = document.getElementById("tag-input");
const tagButton = document.getElementById("tag-button");
const tagContainer = document.getElementById("tag-container");
let tagCounter = 0;


function createTagElement(tagName) {
    const tag = document.createElement("div");
    tag.classList.add("tag");
    tag.textContent = tagName;
    const close = document.createElement("span");
    close.classList.add("tag-close");
    close.textContent = "x";

	
	const tagId = `tag-${tagCounter}`;
	tagCounter++;
	tag.id= tagId;


    close.addEventListener("click", () => {
        tag.remove();
		console.log(`Deleted tag with id ${tag.id}`);
    });
    tag.appendChild(close);
	console.log(`Tag created with id: ${tagId}`);
    return tag;

}

tagButton.addEventListener("click", () => {
	const tagName = tagInput.value.trim();
    if (tagName !== "") {
        const tag = createTagElement(tagName);
        tagContainer.appendChild(tag);
        tagInput.value = "";
    }
});








