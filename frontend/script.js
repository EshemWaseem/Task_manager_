const API = "https://task-manager-u70c.onrender.com/tasks";

async function loadTasks() {
    try {
        const res = await fetch(API);

        if (!res.ok) {
            throw new Error("Failed to fetch tasks");
        }

        const data = await res.json();

        let html = "";

        data.forEach(task => {
            html += `
                <li>
                    <input
                        type="checkbox"
                        ${task.completed ? "checked" : ""}
                        onchange="toggle(${task.id}, '${task.title.replace(/'/g, "\\'")}', this.checked)"
                    >

                    <span style="${task.completed ? 'text-decoration: line-through;' : ''}">
                        ${task.title}
                    </span>

                    <button onclick="editTask(${task.id}, '${task.title.replace(/'/g, "\\'")}', ${task.completed})">
                        Edit
                    </button>

                    <button onclick="removeTask(${task.id})">
                        Delete
                    </button>
                </li>
            `;
        });

        document.getElementById("tasks").innerHTML = html;

    } catch (error) {
        console.error(error);
        alert("Unable to connect to the backend.");
    }
}

async function addTask() {
    const input = document.getElementById("taskInput");
    const title = input.value.trim();

    if (title === "") {
        alert("Please enter a task title.");
        return;
    }

    await fetch(API, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title
        })
    });

    input.value = "";
    loadTasks();
}

async function removeTask(id) {
    await fetch(`${API}/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}

async function toggle(id, title, completed) {
    await fetch(`${API}/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            completed: completed
        })
    });

    loadTasks();
}

async function editTask(id, title, completed) {
    const newTitle = prompt("Edit Task", title);

    if (newTitle === null) return;

    if (newTitle.trim() === "") {
        alert("Task title cannot be empty.");
        return;
    }

    await fetch(`${API}/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: newTitle.trim(),
            completed: completed
        })
    });

    loadTasks();
}

loadTasks();