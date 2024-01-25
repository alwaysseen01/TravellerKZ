document.addEventListener('DOMContentLoaded', function() {
    window.chooseNavigationElement = (element_id) => {
        let nav_elements = document.querySelectorAll('.navigationElement');
        nav_elements.forEach((element) => {
          element.classList.remove('chosen');
        });
        let chosenElement = document.getElementById(element_id);
        chosenElement.classList.add('chosen');
    };  
});
  