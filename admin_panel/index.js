document.addEventListener('DOMContentLoaded', function() {
  window.openPageByChosenNavElement = (chosen_element_id) => {
    let chosen_element = this.getElementById(chosen_element_id);
    let pages = document.querySelectorAll('.commandsInfoPage, .adminsInfoPage, .contentInfoPage');
    pages.forEach((page) => {
      page.classList.remove('opened');
    });

    if (chosen_element.innerHTML == "COMMANDS") {
      let commandsPage = document.getElementById('commandsInfoPage opened');
      commandsPage.classList.add('opened');
    } else if (chosen_element.innerHTML == "ADMIN LIST") {
      let adminsPage = document.getElementById('adminsInfoPage');
      adminsPage.classList.add('opened');
    } else if (chosen_element.innerHTML == "CONTENT") {
      let contentPage = document.getElementById('contentInfoPage');
      contentPage.classList.add('opened');
    }
  }

  window.chooseNavigationElement = (element_id) => {
    let nav_elements = document.querySelectorAll('.navigationElement');
    nav_elements.forEach((element) => {
      element.classList.remove('chosen');
    });
    let chosenElement = document.getElementById(element_id);
    chosenElement.classList.add('chosen');

    // Open page
    openPageByChosenNavElement(element_id)
  };
  
  window.openEditCommandMenu = (button_id) => {
    let editCommandMenu = document.querySelector('.editCommandMenu');
    editCommandMenu.classList.add('opened');
  }

  window.confirmEditCommandMenu = (button_id) => {
    // Some fetch logic
    // ....
    let editCommandMenu = document.querySelector('.editCommandMenu');
    editCommandMenu.classList.remove('opened');
    event.preventDefault();
  }

  window.closeEditCommandMenu = (button_id) => {
    let editCommandMenu = document.querySelector('.editCommandMenu');
    editCommandMenu.classList.remove('opened');
    event.preventDefault();
  }

  window.openAddCommandMenu = (button_id) => {
    let addCommandMenu = document.querySelector('.addCommandMenu');
    addCommandMenu.classList.add('opened');
  }

  window.confirmAddCommandMenu = (button_id) => {
    // Some fetch logic
    // ....
    let addCommandMenu = document.querySelector('.addCommandMenu');
    addCommandMenu.classList.remove('opened');
    event.preventDefault();
  }

  window.closeAddCommandMenu = (button_id) => {
    let addCommandMenu = document.querySelector('.addCommandMenu');
    addCommandMenu.classList.remove('opened');
    event.preventDefault();
  }

  let citySelectors = document.querySelectorAll('.citySelector');
  citySelectors.forEach(function(citySelector) {
    citySelector.addEventListener('change', function() {
      let botResponseInput = this.parentNode.querySelector('input[name="botResponse"]');
      if (this.value !== 'defaultOption') {
        botResponseInput.disabled = true;
      } else {
        botResponseInput.disabled = false;
      }
    });
  });

  window.openAddAdminMenu = (button_id) => {
    let addAdminMenu = document.querySelector('.addAdminMenu');
    addAdminMenu.classList.add('opened');
  }

  window.confirmAddAdminMenu = (button_id) => {
    // Some fetch logic
    // ....
    let addAdminMenu = document.querySelector('.addAdminMenu');
    addAdminMenu.classList.remove('opened');
    event.preventDefault();
  }

  window.closeAddAdminMenu = (button_id) => {
    let addAdminMenu = document.querySelector('.addAdminMenu');
    addAdminMenu.classList.remove('opened');
    event.preventDefault();
  }

  window.openAddCityMenu = (button_id) => {
    let addCityMenu = document.querySelector('.addCityMenu');
    addCityMenu.classList.add('opened');
  }

  window.confirmAddCityMenu = (button_id) => {
    // Some fetch logic
    // ....
    let addCityMenu = document.querySelector('.addCityMenu');
    addCityMenu.classList.remove('opened');
    event.preventDefault();
  }

  window.closeAddCityMenu = (button_id) => {
    let addCityMenu = document.querySelector('.addCityMenu');
    addCityMenu.classList.remove('opened');
    event.preventDefault();
  }
});

  