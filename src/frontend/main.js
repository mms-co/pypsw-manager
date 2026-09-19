const master_key = document.getElementById("master-key");

const save_entry = document.getElementById("save-entry");
const save_psw = document.getElementById("save-psw");

const get_entry = document.getElementById("show-entry");
const get_psw = document.getElementById("show-psw");


const num_regex = /^[0-9]*$/gi;

// Show passwords
Array.from(document.getElementsByClassName("show-opt")).map(e => {
	// Simple DOM navigation, adding onclick event to checkbox,
	// which is located as the first element in switch node,
	// and input which is the first element before switch node
	let parent = e.parentNode;
	let input_field = parent.parentNode.firstElementChild;
	parent.firstElementChild.onclick = () => {
		// Switch text and password types to show
		if (input_field.type == "password") {
			input_field.type = "text";
		} else {
			input_field.type = "password";
		}
	}
});


// Simple pywebview API calls
function save() {
	let password = save_psw.value;
	let entry = save_entry.value;
	let key = master_key.value;
	if (key == "")
		return
	window.pywebview.api.save(key, entry, password);
}

async function get() {
	let entry = get_entry.value;
	let key = master_key.value;
	let res = await window.pywebview.api.get(key, entry);
	if (res.success)
		get_psw.value = res.value;
}


// Make sure user can naturally only put integer values for length
var old_value = '';
function only_numbers(length) {
	if (!length.value.match(num_regex))
		length.value = old_value;
	old_value = length.value;
}


function random_num(from, to) {
	return parseInt(from + (to - from) * Math.random());
}

function generate() {
	// Get all the options
	const length = document.getElementById("psw-length").value;
	if (!length.match(num_regex))
		return false;
	const is_upper = document.getElementById("allow-upper").checked;
	const is_number = document.getElementById("allow-numbers").checked;
	const is_symbol = document.getElementById("allow-symbols").checked;

	// Collect every character option in a pool
	let pool = "abcdefghijklmnopqrstuvwxyz";
	let upper = is_upper ? pool.toUpperCase() : [];
	let number = is_number ? "1234567890" : [];
	let symbol = is_symbol ? "!\"£$%^&*()_+-=[]{}'#@~;:,.<>/?\\`|¬" : [];
	pool = [...pool, ...upper, ...number, ...symbol];
	let password = [];
	for (let i = 0; i < parseInt(length); i++) {
		password[i] = pool[random_num(0, pool.length)];
	}
	save_psw.value = password.join("");
}