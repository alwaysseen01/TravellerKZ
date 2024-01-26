document.addEventListener('DOMContentLoaded', function() {
  window.openPageByChosenNavElement = (chosen_element_id) => {
    let chosen_element = this.getElementById(chosen_element_id);
    let pages = document.querySelectorAll('.commandsInfoPage, .adminsInfoPage');
    pages.forEach((page) => {
      page.classList.remove('opened');
    });

    if (chosen_element.innerHTML == "COMMANDS") {
      let commandsPage = document.getElementById('commandsInfoPage opened');
      commandsPage.classList.add('opened');
    } else if (chosen_element.innerHTML == "ADMIN LIST") {
      let adminsPage = document.getElementById('adminsInfoPage');
      adminsPage.classList.add('opened');
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
  }

  window.closeEditCommandMenu = (button_id) => {
    let editCommandMenu = document.querySelector('.editCommandMenu');
    editCommandMenu.classList.remove('opened');
  }
});

  