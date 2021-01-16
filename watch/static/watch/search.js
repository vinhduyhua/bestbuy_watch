window.addEventListener("DOMContentLoaded", (event) => {

	const item = document.querySelector("#item")

	item.value = ''

	console.log('DOM fully loaded and parsed');

	const search_btn = document.querySelector("#search")

	search_btn.disabled = true;

	// Prevent empty html input
	item.onkeyup = () => {
		if (item.value.length > 0) {
			search_btn.disabled = false;
		} else {
			search_btn.disabled = true;
		}
	}

	// When search button click
	search_btn.onclick = () => {

		const list_item = document.querySelector('.list_item')

		// Refresh list_item
		list_item.innerHTML = ''

		// Get data from django
		fetch(`/search/${item.value}`)
		.then(response => response.json())
		.then(found_items => {

			// When search item does not match
			if (found_items == '') {
				list_item.innerHTML = `<p style="text-align: center;">Could not find any item that match the "${item.value}"</p>`
			}

			found_items.forEach(item => {

				console.log(item)

				const list_item_row = document.createElement('div')
				list_item_row.className = 'row align-items-start'

				const html_title = document.createElement('div')
				html_title.className = 'col';

				const html_price = document.createElement('div')
				html_price.className = 'col-2'

				const html_status = document.createElement('div')
				html_status.className = 'col-2'

				const watch_btn_col = document.createElement('div')
				watch_btn_col.className = 'col-2'

				const watch_btn = document.createElement('button')
				
				fetch(`/get_watch_status/${item.id}`)
				.then(response => response.text())
				.then(text => {
					if (text == "True") {
						watch_btn.className = 'btn btn-secondary'
						watch_btn.innerHTML = 'Unwatch'
					} else {
						watch_btn.className = 'btn btn-info'
						watch_btn.innerHTML = 'Watch'
					}
				}) // End .then text

				watch_btn_col.append(watch_btn)

				// On click watch btn
				watch_btn.onclick = () => {
					console.log("Click watch_btn")

					fetch("/watch", {
						method: "POST",
						credentials: "same-origin",
						body: JSON.stringify ({
							item_id: item.id,
						})
					}) // End of fetch watch

					if (watch_btn.innerHTML == 'Unwatch') {
						watch_btn.className = 'btn btn-info'
						watch_btn.innerHTML = 'Watch'
					} else {
						watch_btn.className = 'btn btn-secondary'
						watch_btn.innerHTML = 'Unwatch'
					}
				}

				html_title.innerHTML = `<a href="http://www.bestbuy.com${item.link}"><p>${item.title}</p></a>`
				html_status.innerHTML = `<p>${item.status}</p>`
				html_price.innerHTML = `<p>\$ ${item.price}</p>`

				list_item_row.append(html_title);
				list_item_row.append(html_status);
				list_item_row.append(html_price);
				list_item_row.append(watch_btn_col);

				list_item.append(list_item_row)

			}) // End forEach item

		}) // End of fetch found items

	} // End of onclick

}) // End DOMContentLoaded