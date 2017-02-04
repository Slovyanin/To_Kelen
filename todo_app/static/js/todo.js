$(document).ready(function () {
    csrf = $('input[name=csrfmiddlewaretoken]').val()
})

// bind events
function bind_events(id) {
    var proj = $('#project_' + id);
    proj.find(".tasks_list").sortable({
        stop: function(event, ui){}
    });
    proj.find(".tasks_list").on("sortstop", function(event, ui){
        // change order in DB
        var ul = $(this).parent('section').find('.tasks_list');
        ul.children('li').each(function( index ){
            $.ajax({
                type: "PATCH",
                url: "/tasks/" + $( this ).attr('id').split('_')[1] + "/",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                data: {priority: ul.children('li').size() - index},
            });
        });
    });
}

function resize_body() {
    var contents_height = $("#header").outerHeight() + $("#content").outerHeight() + $("#footer").outerHeight() + 40;
    $("body").height(Math.max(contents_height, $(window).height()));
}

// add project
function add_project(user_id) {
    $.ajax({
        type: "POST",
        url: "/projects/",
        data: {
            csrfmiddlewaretoken: csrf,
            name: "Click button to change name ->",
            user: user_id,
        }
    }).done(function (data) {
        render_project(data.id);
    });
}

// change project name
function project_init_change_name(id) {
    var section = $('#project_'+id);
    var oldname = section.find('.project-title').text();
    section.find('.project-title').replaceWith('<div class="project-name-change">' +
        '<input type="text" name="project_name" placeholder="Enter project name" value="' + oldname + '">' +
        '<button onclick="project_change_name(' + id + ')">' +
        '<span class="add-words valign-middle">Change</span>' +
        '</button></div>');
}

function project_change_name(id) {
    var section = $('#project_'+id);
    var name = section.find(".project-name-change input").val();
    console.log(csrf)
    $.ajax({
        type: "PATCH",
        url: "/projects/" + id + "/",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        data: {
            name: name
        }
    });
    section.find('.project-name-change').replaceWith('<span class="m-words project-title">' + name + '</span>');
}

// delete project
function project_delete(id) {
    var section = $('#project_'+id);
    section.remove();
    resize_body();
    $.ajax({
        type: "DELETE",
        url: "/projects/" + id + "/",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        }
    });
}

// add task
function add_task(id) {
    var section = $('#project_'+id);
    var task = section.find('.second input').val();
    if(task != ''){
        $.ajax({
            type: "POST",
            url: "/tasks/",
            data: {
                csrfmiddlewaretoken: csrf,
                name: task,
                project: id,
            },
        }).done(function (data) {
            render_task(data.id, id);
        });
    }
    section.find('.second input').val('');
}

// change task
function init_task_change(id) {
    var task_div = $('#task_'+id);
    var oldname = task_div.find('.t-words').text();
    task_div.find('.t-words').replaceWith('<div class="task-change">' +
        '<input type="text" name="task_name" placeholder="Enter task" value="' + oldname + '">' +
        '<button onclick="task_change(' + id + ')">' +
        '<span class="add-words valign-middle">Change</span>' +
        '</button></div>');
}

function task_change(id) {
    var task_div = $('#task_'+id);
    var name = task_div.find(".task-change input").val();
    $.ajax({
        type: "PATCH",
        url: "/tasks/" + id + "/",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        data: {
            name: name,
        },
    });
    task_div.find('.task-change').replaceWith('<span class="t-words">' + name + '</span>');
}

// change task status
function task_status(id) {
    var task_div = $('#task_'+id);
    var status = task_div.find('.checkbox').prop('checked');
    $.ajax({
        type: "PATCH",
        url: "/tasks/" + id + "/",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        data: {
            status: status,
        },
    });
}

// delete task
function task_delete(id) {
    var task_div = $('#task_'+id);
    task_div.remove();
    resize_body();
    $.ajax({
        type: "DELETE",
        url: "/tasks/" + id + "/",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
    });
}

// render project
function render_project(id) {
    var projects = $('#projects');
    $.get( "/render_project/" + id, function( data ) {
        projects.append( data );
        bind_events(id);
        resize_body();
    });
}

// render task
function render_task(id, proj_id) {
    var section = $('#project_'+proj_id);

    $.get( "/render_task/" + id, function( data ) {
        section.find('.tasks_list').append(data);
        var task_div = $("#task_" + id);

        var ul = section.find('.tasks_list'),
        li = ul.children('li');

        li.detach().sort(function(a,b) {
            return $(b).data('sortby') - $(a).data('sortby');
        });

        ul.append(li);

        // deadline
        task_div.find(".dp").datepicker({dateFormat: "yy-mm-dd"});
        task_div.find(".dp").change(function () {
            var date = $(this).val();
            $.when($.ajax({
                type: "PATCH",
                url: "/tasks/" + id + "/",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                data: {
                    deadline: date,
                },
            })).then(function () {
                $.get( "/render_task/" + id, function( againdata ) {
                task_div.find(".t-words").text($(againdata).find(".t-words").text())
                });
            });
        });
        resize_body();
    });
}

function render_all() {
    $.get("/projects/", function( projects ) {
        projects.forEach(function (p_element) {
            $.when(render_project(p_element.id)).then(function () {
               $.get("/project/" + p_element.id + "/tasks/", function (tasks) {
                    tasks.forEach(function (t_element) {
                        render_task(t_element.id, p_element.id);
                    })
                })
            });
        });
    });
}

function show_datepicker(id) {
    $("#task_" + id).find(".dp").datepicker('show');
}
