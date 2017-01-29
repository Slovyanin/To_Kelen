
// sortable list of tasks
$(function () {
    $(".tasks_list").sortable({
      stop: function(event, ui){}
    });
});
$(".tasks_list").on("sortstop", function(event, ui){
    // change order in DB
});

// change project name
function project_init_change_name(id) {
    var section = $('#'+id);
    var oldname = section.find('.project-title').text();
    section.find('.project-title').replaceWith('<div class="project-name-change">' +
        '<input type="text" name="project_name" placeholder="Enter project name" value="' + oldname + '">' +
        '<button onclick="project_change_name(' + id + ')">' +
        '<span class="add-words valign-middle">Change</span>' +
        '</button></div>');
}

function project_change_name(id) {
    var section = $('#'+id);
    var name = section.find(".project-name-change input").val();
    // change name in DB
    section.find('.project-name-change').replaceWith('<span class="m-words project-title">' + name + '</span>');
}


// delete project
function project_delete(id) {
    var section = $('#'+id);
    section.remove();
    // delete project in DB
}

// add task
function add_task(id) {
    var section = $('#'+id);
    var task = section.find('.second input').val();
    // add task to DB
    section.find('.tasks_list').append('<div class="third" id="123"><div><input type="checkbox"/></div>' +
        '<div><span class="t-words">' + task + '</span></div>' +
        '<div><img src="/static/images/arrowt.png"></div>' +
        '<div><a href="javascript:init_task_change(123)"><img src="/static/images/notemt.png"></a></div>' +
        '<div><a href="#"><img src="/static/images/backetmt.png"></a></div>' +
        '</div>');
}

//change task
function init_task_change(id) {
    var task_div = $('#'+id);
    var oldname = task_div.find('.t-words').text()
    task_div.find('.t-words').replaceWith('<div class="task-change">' +
        '<input type="text" name="task_name" placeholder="Enter task" value="' + oldname + '">' +
        '<button onclick="task_change(' + id + ')">' +
        '<span class="add-words valign-middle">Change</span>' +
        '</button></div>');
}

function task_change(id) {
    var task_div = $('#'+id);
    var name = task_div.find(".task-change input").val();
    // change task in DB
    task_div.find('.task-change').replaceWith('<span class="t-words">' + name + '</span>');
}

//delete task
function task_delete(id) {
    var task_div = $('#'+id);
    task_div.remove();
    //remove task from DB
}
