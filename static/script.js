const API="/tasks";

async function loadTasks(){

const res=await fetch(API);

const data=await res.json();

let html="";

data.forEach(task=>{

html+=`
<li>

<input type="checkbox"
${task.completed?"checked":""}
onclick="toggle(${task.id},
'${task.title}',
this.checked)">

${task.title}

<button onclick="editTask(${task.id},
'${task.title}',
${task.completed})">
Edit
</button>

<button onclick="removeTask(${task.id})">
Delete
</button>

</li>
`;

});

document.getElementById("tasks").innerHTML=html;

}

async function addTask(){

const title=document.getElementById("taskInput").value;

await fetch(API,{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({title})
});

document.getElementById("taskInput").value="";

loadTasks();

}

async function removeTask(id){

await fetch(API+"/"+id,{
method:"DELETE"
});

loadTasks();

}

async function toggle(id,title,status){

await fetch(API+"/"+id,{
method:"PUT",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
title:title,
completed:status
})
});

loadTasks();

}

async function editTask(id,title,completed){

const newTitle=prompt("Edit Task",title);

if(newTitle){

await fetch(API+"/"+id,{
method:"PUT",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
title:newTitle,
completed:completed
})
});

loadTasks();

}

}

loadTasks();