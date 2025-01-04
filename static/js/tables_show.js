const buttons = document.querySelectorAll('.table_btn');
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const hiddens = document.querySelectorAll('.'+button.id);
        hiddens.forEach(hidden => {
            console.log(hidden.id);
            hidden.classList.remove('hidden');
        });
        const row = document.getElementById('btn_'+button.id);
        row.classList.add('hidden');
    });
});