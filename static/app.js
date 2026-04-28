const API_BASE = "";

async function createHabit() {
    const name = document.getElementById("habitName").value;
    const type = document.getElementById("habitType").value;

    const res = await fetch("/habits/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: name,
            type: type,
            meta: {}
        })
    });

    const data = await res.json();
    alert("Created: " + data.id);
    document.getElementById("habitName").value = "";
    document.getElementById("habitType").value = "";
    loadHabits();
}

async function loadHabits(showArchived = false) {
    let url = "/habits/";
    if (showArchived) {
        url = "/habits/archived";
    }

    const res = await fetch(url);
    const habits = await res.json();

    const list = document.getElementById("habitList");
    list.innerHTML = "";

    if (!habits || habits.length === 0) {
        list.innerHTML = "<li>No habits found</li>";
        return;
    }

    habits.forEach(h => {
        const li = document.createElement("li");

        if (showArchived) {
            li.className = "archived-item";
            li.innerHTML = `
                ${h.name} (${h.type})
                <button class="secondary" onclick="restoreHabit('${h.id}')">Restore</button>
                <button class="danger" onclick="deleteHabit('${h.id}')">Delete</button>
            `;
        } else {
            li.innerHTML = `
                ${h.name} (${h.type})
                <button onclick="editHabit('${h.id}', '${h.name}')">Edit</button>
                <button onclick="archiveHabit('${h.id}')">Archive</button>
                <button class="danger" onclick="deleteHabit('${h.id}')">Delete</button>
            `;
        }

        list.appendChild(li);
    });
}

async function loadProgress() {
    const date = document.getElementById("progressDate").value;

    if (!date) {
        alert("Please enter a date");
        return;
    }

    try {
        const res = await fetch(`/progress?date=${date}`);
        const data = await res.json();

        document.getElementById("progressOutput").textContent =
            JSON.stringify(data, null, 2);
    } catch (err) {
        document.getElementById("progressOutput").textContent = "Error: " + err.message;
    }
}

async function editHabit(id, currentName) {
    const newName = prompt("New habit name:", currentName);

    if (!newName) return;

    try {
        const res = await fetch(`/habits/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: newName,
                meta: {}
            })
        });

        if (!res.ok) {
            const error = await res.json();
            alert("Error: " + error.detail);
            return;
        }

        loadHabits();
    } catch (err) {
        alert("Error updating habit: " + err.message);
    }
}

async function archiveHabit(id) {
    if (!confirm("Are you sure you want to archive this habit?")) return;

    try {
        const res = await fetch(`/habits/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            const error = await res.json();
            alert("Error: " + error.detail);
            return;
        }

        loadHabits();
    } catch (err) {
        alert("Error archiving habit: " + err.message);
    }
}

async function restoreHabit(id) {
    try {
        const res = await fetch(`/habits/${id}/restore`, {
            method: "PUT"
        });

        if (!res.ok) {
            const error = await res.json();
            alert("Error: " + error.detail);
            return;
        }

        loadHabits(true);
    } catch (err) {
        alert("Error restoring habit: " + err.message);
    }
}

async function deleteHabit(id) {
    if (!confirm("Permanently delete this habit? This cannot be undone.")) return;

    try {
        const res = await fetch(`/habits/${id}/permanent`, {
            method: "DELETE"
        });

        if (!res.ok) {
            const error = await res.json();
            alert("Error: " + error.detail);
            return;
        }

        loadHabits();
    } catch (err) {
        alert("Error deleting habit: " + err.message);
    }
}

// Load active habits on page load
document.addEventListener("DOMContentLoaded", () => loadHabits(false));
