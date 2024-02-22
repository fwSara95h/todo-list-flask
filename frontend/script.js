document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
    document.getElementById('todoForm').addEventListener('submit', addTodo);
});

async function fetchTodos() {
    const response = await fetch('/todos');
    const todos = await response.json();
    const todoList = document.getElementById('todoList');
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = todo.completed;
        checkbox.onchange = () => toggleCompleted(todo.id, checkbox.checked);
        
        const text = document.createTextNode(` ${todo.task}`);
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteTodo(todo.id);
        
        li.appendChild(checkbox);
        li.appendChild(text);
        li.appendChild(deleteButton);
        todoList.appendChild(li);
    });
}

async function addTodo(event) {
    event.preventDefault();
    const taskInput = document.getElementById('taskInput');
    const task = taskInput.value;
    if (task) {
        await fetch('/todo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task }),
        });
        taskInput.value = ''; // Clear input after submission
        fetchTodos(); // Refresh the list
    }
}

async function toggleCompleted(id, completed) {
    await fetch(`/todo/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed }),
    });
    fetchTodos(); // Refresh the list to reflect the change
}

async function deleteTodo(id) {
    await fetch(`/todo/${id}`, {
        method: 'DELETE',
    });
    fetchTodos(); // Refresh the list to reflect the deletion
}
