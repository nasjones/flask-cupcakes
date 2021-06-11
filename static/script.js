const CUPCAKE_API_ENDPOINT = "/api";
async function get_cupcakes() {
	try {
		let response = await axios.get(`${CUPCAKE_API_ENDPOINT}/cupcakes`);
		appendCupcakes(response.data.cupcakes);
	} catch (GETERROR) {
		alert("Sorry there was a problem getting the cupcakes.");
	}
}

function appendCupcakes(cupcakes) {
	for (let cupcake of cupcakes) {
		addToList(cupcake);
	}
}

function addToList(cupcake) {
	let listItem = document.createElement("li");
	let image = document.createElement("img");
	let description = document.createElement("p");
	let rating = document.createElement("p");
	$(image).attr("src", cupcake.image);
	$(description).text(`A ${cupcake.size} ${cupcake.flavor} cupcake.`);
	$(rating).text(`Rating: ${cupcake.rating}/10`);

	$(listItem).append(image, description, rating);
	$(listItem).addClass("cupcake-list-item");
	$("#cupcake-list").append(listItem);
}

async function newCupcake(e) {
	e.preventDefault();
	let values = {};
	let newForm = $(e.target);
	for (let item of newForm.find("input")) {
		values[item.name] = item.value;
	}
	try {
		let request = await axios.post(
			`${CUPCAKE_API_ENDPOINT}/cupcakes`,
			values
		);
		addToList(request.data.cupcake);
	} catch (POSTERROR) {
		alert("Sorry there was an error adding your cupcake.");
	}
}

$(document).on("ready", get_cupcakes());
$("#new-cupcake-form").on("submit", (e) => newCupcake(e));
