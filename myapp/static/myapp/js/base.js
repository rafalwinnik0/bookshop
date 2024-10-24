function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addToCart(bookId) {

    if (isAuthenticated === "true") {
        fetch('/add-to-cart/' + bookId + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 'book_id': bookId })
        })
        .then(response => {
            if(response.ok) {
                return response.json();
            }
            throw new Error('Coś poszło nie tak z siecią.');
        })
        .then(data => {
            console.log("Odpowiedź serwera:", data);
            alert("Książka została dodana do koszyka!");
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } else {
        alert("Zaloguj się, aby dodać element do koszyka");
    }
}

function removeFromCart(itemId) {
    let totalPrice = document.getElementById('totalCart');
    fetch('/remove-from-cart/' + itemId + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'item_id': itemId})
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            let itemElement = document.getElementById('item-' + itemId)
            if (itemElement) {
                itemElement.remove();
                totalPrice.innerHTML = "$" + data.total;
            }
            alert("Książka została usunięta z koszyka!");
        } else {
            alert("Wystąpił błąd: " + data.error);
        }
    });
}

function removeAddress(addressId) {
    fetch('/remove-address/' + addressId + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'address_id': addressId})
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            let addressElement = document.getElementById('address-' + addressId)
            if (addressElement) {
                addressElement.remove();
             }
            alert("Adres usunięty!");
        } else {
            alert("Wystąpił błąd: " + data.error);
        }
    });
}

function changeQuantity(button, change) {
    let itemId = button.getAttribute('data-item-id');
    let quantityInput = document.getElementById('quantity-' + itemId);
    let currentQuantity = parseInt(quantityInput.value);
    let newQuantity = currentQuantity + change;
    let productPrice = document.getElementById('total-price-' + itemId);
    let totalPrice = document.getElementById('totalCart');

    if (newQuantity >= 0) {
        fetch('/update-quantity/' + itemId + '/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'quantity': newQuantity})

        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                quantityInput.value = data.new_quantity;
                productPrice.innerHTML = data.new_value + " zł";
                totalPrice.innerHTML = data.total + " zł";

            } else {
                alert("Nie można zaktualizować ilości");
            }
        });
    }
}

function fillAddress() {
    fetch('/fill-address/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            document.getElementById('firstName').value = data.first_name;
            document.getElementById('lastName').value = data.last_name;
            document.getElementById('address').value = data.address;
            document.getElementById('zipCode').value = data.zip_code;
            document.getElementById('country').value = data.country;
        } else {
            alert("There is no user address!");
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    let editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            let firstName = btn.getAttribute('data-first-name');
            let lastName = btn.getAttribute('data-last-name');
            let address = btn.getAttribute('data-address');
            let zip = btn.getAttribute('data-zip');
            let country = btn.getAttribute('data-country');
            let id = btn.getAttribute('data-id');

            document.getElementById('modalFirstName').value = firstName;
            document.getElementById('modalLastName').value = lastName;
            document.getElementById('modalAddress').value = address;
            document.getElementById('modalZip').value = zip;
            document.getElementById('modalCountry').value = country;
            document.getElementById('modalAddressId').value = id;
        });
    });
 });

function saveChanges() {
let addressId = document.getElementById('modalAddressId').value;
let firstName = document.getElementById('modalFirstName').value;
let lastName = document.getElementById('modalLastName').value;
let address = document.getElementById('modalAddress').value;
let zip = document.getElementById('modalZip').value;
let country = document.getElementById('modalCountry').value;

fetch('/update-address/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-CSRFToken': '{{ csrf_token }}'
    },
    body: new URLSearchParams({
        'address_id': addressId,
        'first_name': firstName,
        'last_name': lastName,
        'address': address,
        'zip_code': zip,
        'country': country
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        document.getElementById('address-'+ addressId + '-kraj').innerHTML = "Kraj: " + country;
        document.getElementById('address-'+ addressId + '-kod').innerHTML = "Kod pocztowy: " + zip;
        document.getElementById('address-'+ addressId + '-adres').innerHTML = "Adres: " + address;
    }
    else {
        console.log('error');
    }
})
.catch(error => {

});
}

document.addEventListener('DOMContentLoaded', function () {
    let editAddressModalEl = document.getElementById('editAddressModal');
    if (editAddressModalEl){
        let editAddressModal = new bootstrap.Modal(editAddressModalEl);
        let saveChangesButton = document.getElementById('saveChangesButton');
        if (saveChangesButton) {
            saveChangesButton.addEventListener('click', function() {
                saveChanges();
                editAddressModal.hide();
            })
        }
    }

});

document.addEventListener('DOMContentLoaded', function () {
    let editAccountBtn = document.getElementById('edit-account-btn');
    if (editAccountBtn) {
        editAccountBtn.addEventListener('click', function(event) {
            let firstName = this.getAttribute('data-first-name');
            let lastName = this.getAttribute('data-last-name');
            let email = this.getAttribute('data-email');
            let username = this.getAttribute('data-username');

            document.getElementById('modalAccountFirstName').value = firstName;
            document.getElementById('modalAccountLastName').value = lastName;
            document.getElementById('modalAccountUsername').value = username;
            document.getElementById('modalAccountEmail').value = email;
        })
    }
});

function saveAccount() {
    let newFirstName  = document.getElementById('modalAccountFirstName').value;
    let newLastName  = document.getElementById('modalAccountLastName').value;
    let newUsername  = document.getElementById('modalAccountUsername').value;
    let newEmail  = document.getElementById('modalAccountEmail').value

    fetch('/update-account/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: new URLSearchParams({
            'new_first_name': newFirstName,
            'new_last_name': newLastName,
            'new_username': newUsername,
            'new_email': newEmail
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('accountEmail').innerHTML = newEmail;
            document.getElementById('accountUsername').innerHTML = newUsername;
        }
        else {
            console.log('error');
        }
    })
    .catch(error => {

    });
}

document.addEventListener('DOMContentLoaded', function () {
    let editAccountModalEl = document.getElementById('editAccountModal');
    if (editAccountModalEl){
        let editAccountModal = new bootstrap.Modal(editAccountModalEl);
        let saveAccountModalButton = document.getElementById('saveAccountModalButton');
        if (saveAccountModalButton) {
            saveAccountModalButton.addEventListener('click', function(event) {
                saveAccount();
                editAccountModal.hide();
            })
        }
    }

});

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('navBarSearchInput');
    const dropdownMenu = document.createElement('ul');
    dropdownMenu.classList.add('dropdown-menu');
    dropdownMenu.classList.add('dropdown-menu-search');
    searchInput.parentNode.appendChild(dropdownMenu);

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length > 0) {
            fetch(`/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                dropdownMenu.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(book => {
                        const listItem = document.createElement('li');
                        listItem.classList.add('dropdown-item');

                        const link = document.createElement('a');
                        link.classList.add('text-decoration-none');
                        link.href = `/${book.id}/`;
                        link.style.display = 'flex';
                        link.style.alignItems = 'center';

                        const image = document.createElement('img');
                        image.src = book.file;
                        image.alt = `${book.title} cover`;
                        image.style.width = '50px';
                        image.style.marginRight = '10px';

                        const textContainer = document.createElement('div');
                        textContainer.classList.add('custom-link');


                        const title = document.createElement('h6');
                        title.textContent = book.title;
                        title.style.margin = '0';

                        const author = document.createElement('p');
                        author.textContent = book.author;
                        author.style.margin = '0';

                        const price = document.createElement('p');
                        price.textContent = `Cena: ${book.price} zł`;
                        price.style.fontWeight = 'bold';
                        price.style.margin = '0';

                        textContainer.appendChild(title);
                        textContainer.appendChild(author);
                        textContainer.appendChild(price);

                        link.appendChild(image);
                        link.appendChild(textContainer);

                        listItem.appendChild(link);

                        dropdownMenu.appendChild(listItem);
                    });
                } else {
                    const noResults = document.createElement('li');
                    noResults.classList.add('dropdown-item');
                    noResults.textContent = 'Brak wyników';
                    dropdownMenu.appendChild(noResults);
                }


                dropdownMenu.classList.add('show');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {

            dropdownMenu.classList.remove('show');
            dropdownMenu.innerHTML = '';
        }
    });

    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});

function showFormResults () {
    let authorCheckboxes = document.querySelectorAll('.form-check-input-author');
    let categoryCheckBoxes = document.querySelectorAll('.form-check-input-category')

    let authorCheckedValues = [];
    authorCheckboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            authorCheckedValues.push(checkbox.id);
        }
    });

    let categoryCheckedValues = [];
    categoryCheckBoxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            categoryCheckedValues.push(checkbox.id);
        }
    });

    let minRange = document.getElementById('minRange').value;
    let maxRange = document.getElementById('maxRange').value;
    let selectedSorting = document.getElementById('sort-options').value;

    let data = {
        authorCheckedValues: authorCheckedValues,
        categoryCheckedValues: categoryCheckedValues,
        minRange: minRange,
        maxRange: maxRange,
        selectedSorting: selectedSorting
    };

    fetch('/search-based-on-filter/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let booksContainer = document.getElementById('books-container');
            let booksNav = document.getElementById('nav-ul');
            booksContainer.innerHTML = '';
            booksNav.innerHTML = '';

            console.log("Received books data", data.books);

            data.books.forEach(function (book) {

                let bookCard = `
                <div class="card d-flex flex-column border border-secondary" style="border:none;">
                    <a href="/${book.id}/">
                        <img src="${book.file}" class="card-img-top" alt="" style="width: 80%;">
                    </a>
                    <div class="text-start py-2">
                        <h5 class="card-subtitle fw-bold fs-6">${book.title}</h5>
                        <p class="card-subtitle">
                            <a class="custom-link" style="font-size:12px;" href="/author/${book.author}/">${book.author}</a>
                        </p>
                        <p class="card-subtitle fw-bold fs-5">${book.price} zł</p>
                    </div>
                    <button onclick="addToCart(${book.id})" class="btn btn-sm btn-danger text-nowrap mt-auto rounded-pill">
                        Dodaj do koszyka
                        <i class="fa fa-shopping-cart"></i>
                    </button>
                </div>
                `;
                booksContainer.innerHTML += bookCard;
            });
            let has_pr = '';
            if (data.page_obj.has_previous) {
                has_pr = `
                <li class="page-item">
                    <a class="page-link" href="/category/?page=${data.page_obj.page_number - 1}" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                `;
            } else {
                has_pr = `
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                `;
            }
            booksNav.innerHTML += has_pr;

            data.page_obj.page_range.forEach(function (num) {
                let liPage = `
                <li class="page-item ${data.page_obj.page_number === num ? 'active' : ''}">
                    <a class="page-link" href="/category/?page=${num}">${num}</a>
                </li>
                `;
                booksNav.innerHTML += liPage;
            });
            let has_next = '';
            if (data.page_obj.has_next) {
                has_next = `
                <li class="page-item">
                    <a class="page-link" href="/category/?page=${data.page_obj.page_number + 1}" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
                `;
            } else {
                has_next = `
                <li class="page-item disabled">
                    <a class="page-link" href="#" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
                `;
            }
            booksNav.innerHTML += has_next;


        } else {
            console.log("Error receiving data from server.");
        }
    })
    .catch((error) => {
        console.error('Błąd podczas wysyłania danych:', error);
    });
}

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function newsletterCommunicat(event) {
    event.preventDefault();
    const newsInput = document.getElementById('newsletterInput');
    const email = newsInput.value;
    if (email) {
        if (isValidEmail(email)) {
            newsInput.value = '';
            alert("Thank you for joining to our society!");
        } else {
            alert("Enter correct email address!")
        }
    } else {
        alert("Email address can not be empty!");
    }

}

function retrieveFromSessionStorage() {
    let savedAuthors = JSON.parse(sessionStorage.getItem('authors') || '[]');
    savedAuthors.forEach(author => {
        let checkbox = document.querySelector(`input[name="author"][value="${author}"]`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });

    let savedCategories = JSON.parse(sessionStorage.getItem('categories') || '[]');
    savedCategories.forEach(category => {
        let categoryCheckbox = document.querySelector(`input[name="category"][value="${category}"]`);
        if (categoryCheckbox) {
            categoryCheckbox.checked = true;
        }
    });

    let stars = JSON.parse(sessionStorage.getItem('stars') || '[]');
    stars.forEach(star => {
        let starCheckbox = document.querySelector(`input[name="stars"][value="${star}"]`);
        if (starCheckbox) {
            starCheckbox.checked = true;
        }
    });
    let accessibility = JSON.parse(sessionStorage.getItem('accessibility') || '[]');
    accessibility.forEach(access => {
        let accessCheckbox = document.querySelector(`input[name="accessibility"][value="${access}"]`);
        if (accessCheckbox) {
            accessCheckbox.checked = true;
        }
    });

    let trend = JSON.parse(sessionStorage.getItem('trend') || '[]');
    trend.forEach(tr => {
        let trendCheckbox = document.querySelector(`input[name="trend"][value="${tr}"]`);
        if (trendCheckbox) {
            trendCheckbox.checked = true;
        }
    });

    let newness = JSON.parse(sessionStorage.getItem('newness') || '[]');
    newness.forEach(nw => {
        let newnessCheckbox = document.querySelector(`input[name="newness"][value="${nw}"]`);
        if (newnessCheckbox) {
            newnessCheckbox.checked = true;
        }
    });

    let minRange = sessionStorage.getItem('minRange');
    let maxRange = sessionStorage.getItem('maxRange');

    if (minRange) {
        document.querySelector('input[name="minRange"]').value = minRange;
    }
    if (maxRange) {
        document.querySelector('input[name="maxRange"]').value = maxRange;
    }
}

function clearFiltersFromSessionStorage() {
    sessionStorage.removeItem('authors');
    sessionStorage.removeItem('categories');
    sessionStorage.removeItem('stars');
    sessionStorage.removeItem('accessibility');
    sessionStorage.removeItem('newness');
    sessionStorage.removeItem('trend');
    sessionStorage.removeItem('minRange');
    sessionStorage.removeItem('maxRange');
}

function applyFilters(page = 1) {

    let authors = [];
    document.querySelectorAll('input[name="author"]:checked').forEach((checkbox) => {
        authors.push(checkbox.value);
    });

    let categories = [];
    document.querySelectorAll('input[name="category"]:checked').forEach((checkbox) => {
        categories.push(checkbox.value);
    });

    let accessibility = [];
    document.querySelectorAll('input[name="accessibility"]:checked').forEach((checkbox) => {
        accessibility.push(checkbox.value);
    });

    let trend = [];
    document.querySelectorAll('input[name="trend"]:checked').forEach((checkbox) => {
        trend.push(checkbox.value);
    });

    let newness = [];
    document.querySelectorAll('input[name="newness"]:checked').forEach((checkbox) => {
        newness.push(checkbox.value);
    });

    let stars = [];
    document.querySelectorAll('input[name="stars"]:checked').forEach((checkbox) => {
        stars.push(checkbox.value);
    });

    let minRange = document.getElementById('minRange').value;
    let maxRange = document.getElementById('maxRange').value;
    let selectedSorting = document.getElementById('sort-options').value;

//    sessionStorage.setItem('authors', JSON.stringify(authors));
//    sessionStorage.setItem('categories', JSON.stringify(categories));
//    sessionStorage.setItem('accessibility', JSON.stringify(accessibility));
//    sessionStorage.setItem('trend', JSON.stringify(trend));
//    sessionStorage.setItem('newness', JSON.stringify(newness));
//    sessionStorage.setItem('stars', JSON.stringify(stars));
//
//    sessionStorage.setItem('minRange', minRange);
//    sessionStorage.setItem('maxRange', maxRange);

    let params = new URLSearchParams();

    authors.forEach((author) => {
        params.append('author', author);
    });

    categories.forEach((category) => {
        params.append('category', category);
    });

    accessibility.forEach((access) => {
        params.append('accessibility', access)
    });

    trend.forEach((tr) => {
        params.append('trend', tr);
    });

    newness.forEach((nw) => {
        params.append('newness', nw);
    });

    stars.forEach((star) => {
        params.append('stars', star);
    });

    if (minRange) params.append('minRange', minRange);
    if (maxRange) params.append('maxRange', maxRange);

    if (selectedSorting) params.append('selected_sorting', selectedSorting);

    params.append('page', page);

    window.location.href = `/new-filter/?${params.toString()}`;

}

//LOADING FILTERS
window.onload = function() {
    var url = new URL(window.location.href);
    var searchParams = new URLSearchParams(url.search);
    searchParams.getAll('author').forEach((author) => {
        let checkbox = document.querySelector(`input[name="author"][value="${author}"]`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    searchParams.getAll('category').forEach((category) => {
        let checkbox = document.querySelector(`input[name="category"][value="${category}"]`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    searchParams.getAll('accessibility').forEach((access) => {
        let checkbox = document.querySelector(`input[name="accessibility"][value="${access}"]`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    searchParams.getAll('trend').forEach((tr) => {
        let checkbox = document.querySelector(`input[name="trend"][value="${tr}"]`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });
    var nw = searchParams.get('newness');
    let checkbox = document.querySelector(`input[name="newness"][value="${nw}"]`);
    if (checkbox) {
        checkbox.checked = true;
    }
    searchParams.getAll('stars').forEach((star) => {
        let checkbox = document.querySelector(`input[name="stars"][value="${star}"]`);
        if (checkbox) {
            checkbox.checked = true;
        }
    });

    minRange = searchParams.get('minRange');
    if (minRange) {
        document.querySelector('input[name="minRange"]').value = minRange;
    }
    maxRange = searchParams.get('maxRange');
    if (maxRange) {
        document.querySelector('input[name="maxRange"]').value = maxRange;
    }

};

function increaseAndExecuteFunction(pageNum) {
    applyFilters(pageNum + 1);
}

function decreaseAndExecuteFunction(pageNum) {
    applyFilters(pageNum - 1);
}

function cleanFilters() {
    document.querySelector('input[name="minRange"]').value = '';
    document.querySelector('input[name="maxRange"]').value = '';
    document.querySelectorAll('input[type="checkbox"]:checked').forEach((checkbox) => {
        checkbox.checked = false;
    });

}

const sortOptions = document.getElementById('sort-options');
if (sortOptions) {
    sortOptions.addEventListener('change', function() {
        applyFilters(1);
    });
}

function setAuthor(author) {
    clearFiltersFromSessionStorage();
    let authors = [];
    authors.push(author);
//    sessionStorage.setItem('authors', JSON.stringify(authors));
    params = new URLSearchParams;
    params.append('author', author);
    window.location.href = `/new-filter/?${params.toString()}`;

}

function setCategory(category) {
    clearFiltersFromSessionStorage();
    let categories = [];
    categories.push(category);
    sessionStorage.setItem('categories', JSON.stringify(categories));
    params = new URLSearchParams;
    params.append('category', category);
    window.location.href = `/new-filter/?${params.toString()}`;

}

function changePage(value) {
    console.log(value);
    console.log(typeof(value));
    var url = new URL(window.location.href);
    console.log(url);
    url.searchParams.set('page', value);
    console.log(url);
    window.location.href = url;
}