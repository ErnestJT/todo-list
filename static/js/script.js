const categoryForm = document.getElementById('category-select-form')
const categoryField = document.getElementById('category-select-field');


categoryField.addEventListener('change', function () {
    categoryForm.submit()
})

const addCategoryField = document.getElementById('category-add-field')

addCategoryField.addEventListener('focus', function (){
    if (this.value === 'Add a new category...') {
        this.value = ""
    }
})

addCategoryField.addEventListener('blur', function (){
    if (this.value.trim() === '') {
        this.value = "Add a new category..."
    }
})

const taskAddField = document.getElementById('task-add-field')

taskAddField.addEventListener('focus', function (){
    if (this.value === 'Add a new task...') {
        this.value = ""
    }
})

taskAddField.addEventListener('blur', function (){
    if (this.value.trim() === '') {
        this.value = "Add a new task..."
    }
})

const checkboxForms = document.querySelectorAll('#checkbox-form')

for (let form of checkboxForms){
    form.addEventListener('change', function(){
        form.submit()
})}

const editIcons = document.querySelectorAll('a#open')
const modalContainer = document.getElementById('modal-container')
const close = document.getElementById('close')

const editForm = document.querySelector('.task-edit-form')
const colorField = document.querySelector('.task-edit-form input[type=color]')
const nameField = document.querySelector('.task-edit-form input[type=text]')
const dateField = document.querySelector('.task-edit-form input[type=date]')

for (let icon of editIcons){
    icon.addEventListener('click', function(){
        modalContainer.classList.add('show')

        const taskID = icon.getAttribute('data-task-id')
        editForm.setAttribute('action', `/edit-task/${taskID}`)

        fetch(`/get-task/${taskID}`, {
            "method": "POST",
        })
        .then(response => response.json())
        .then((body) => {
            colorField.value = body['color']
            nameField.value = body['task_description']
            
            if (body['due_date'] !== 'N/A') {
                dateField.value = body['due_date']
            }
        })
    })
}

window.addEventListener('click', e => {
    e.target === modalContainer ? modalContainer.classList.remove('show') : false;
})
    
close.addEventListener('click', function(){
    modalContainer.classList.remove('show')
})
        

