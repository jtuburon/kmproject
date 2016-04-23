/*
-------------------------------------------------
Session Functions
-------------------------------------------------
*/
function login(){
	if($('#loginModal')){
		$('#loginModal').modal('show')
	}
}

function do_login(){
	var username= $('#username').val();
	var password= $('#password').val();
	
	data = {
		username: username, 
		password: password, 
	};
	$.ajax({
	    type: "POST",
	    url: "users/login",
	    dataType: "json",
	    data: data,
	    success: function (response) {
			if(response.status==1){
				location.reload(true);
			}
	    },
	    error: function (request, status, err) {
	    	console.log(err);
	    }
	});
}

function logout(){
	$.ajax({
	    type: "POST",
	    url: "users/logout",
	    dataType: "json",
	    success: function (response) {
			if(response.status==1){
				location.reload(true);
			}else{
				$('#loginModal').modal('hide');
			}
	    },
	    error: function (request, status, err) {
	    	console.log(err);
	    }
	});
}

/*
-------------------------------------------------
User's Admin Functions
-------------------------------------------------
*/

function users_index(){
    $('#page-wrapper').load('users/main', function(){
    	$('#users_filter_text').bind("enterKey",function(e){
           filter_users(1);
        });
        $('#users_filter_text').keyup(function(e){
            if(e.keyCode == 13)
            {
                $(this).trigger("enterKey");
            }
        });
        filter_users(1)
    });
}

function filter_users(page){
	var filter_text= $('#users_filter_text').val();
	var filter_type= $('#users_filter_type').val();
	data = {filter_type: filter_type, filter_text: filter_text, page: page}
	$('#users_div').load('users/filter', data);
}

/*
-------------------------------------------------
Info Functions
-------------------------------------------------
*/

function info_index(){
    $('#page-wrapper').load('info/main');
}

/*
-------------------------------------------------
Lessons Functions
-------------------------------------------------
*/
function lessons_index(){
    $('#page-wrapper').load('lessons/index', function(){
        search_lessons(1)
    });
}

function lessons_admin(){
    $('#page-wrapper').load('lessons/main', function(){
    	$('#lessons_filter_text').bind("enterKey",function(e){
           filter_lessons(1);
        });
        $('#lessons_filter_text').keyup(function(e){
            if(e.keyCode == 13)
            {
                $(this).trigger("enterKey");
            }
        });
        filter_lessons(1)
    });
}

function search_lessons(page){
	var query_tags= $("#lessons_tags_query").tagsinput('items')
	data = {query_tags: query_tags, page: page}
	$('#lessons_div').load('lessons/search', data);
}

function filter_lessons(page){
	var filter_type= $('#lessons_filter_type').val();
	var filter_text= $('#lessons_filter_text').val();
	data = {filter_type: filter_type, filter_text: filter_text, page: page}
	$('#lessons_div').load('lessons/filter', data);
}

function new_lesson(){
	$('#lesson_form').html('');
	$('#lesson_form').load('lessons/new', function(){
		if($('#lessonModal')){
			$('#lessonModal').modal('show')
		}
	});
}

function create_lesson(){
	var project= $('#project').val();
	var leader= $('#leader').val();
	var author= $('#author').val();
	var role= $('#role').val();
	var title= $('#title').val();
	var problem= $('#problem').Editor("getText");
	var context= $('#context').Editor("getText");
	var solution= $('#solution').Editor("getText");
	
	data = {
		project: project, 
		leader: leader, 
		author: author, 
		role: role, 
		title: title, 
		problem: problem, 
		context: context, 
		solution: solution
	};
	$.ajax({
	    type: "POST",
	    url: "lessons/create",
	    dataType: "json",
	    data: data,
	    success: function (response) {
			console.log(response)
			if(response.status==1){
				$('#lessonModal').modal('hide');
				search_lessons(1);
			}

	    },
	    error: function (request, status, err) {
	    	console.log(err);
	    }
	});
}

function lesson_edit(lesson_id){
	data= {lesson_id: lesson_id};
    $('#lesson_form').html('');
	$('#lesson_form').load('lessons/edit', data,  function(){
		if($('#lessonModal')){
			$('#lessonModal').modal('show')
		}
	});
}

function update_lesson(){
	var lesson_id= $('#number').val();
	var project= $('#project').val();
	var leader= $('#leader').val();
	var author= $('#author').val();
	var role= $('#role').val();
	var title= $('#title').val();
	var problem= $('#problem').Editor("getText");
	var context= $('#context').Editor("getText");
	var solution= $('#solution').Editor("getText");
	
	data = {
		lesson_id: lesson_id,
		project: project, 
		leader: leader, 
		author: author, 
		role: role, 
		title: title, 
		problem: problem, 
		context: context, 
		solution: solution
	};
	$.ajax({
	    type: "POST",
	    url: "lessons/update",
	    dataType: "json",
	    data: data,
	    success: function (response) {
			console.log(response)
			if(response.status==1){
				$('#lessonModal').modal('hide');
				filter_lessons(1);
			}

	    },
	    error: function (request, status, err) {
	    	console.log(err);
	    }
	});
}

function lesson_show(lesson_id){
	data= {lesson_id: lesson_id};
    $('#lesson_form').html('');
	$('#lesson_form').load('lessons/show', data,  function(){
		if($('#lessonModal')){
			$('#lessonModal').modal('show')
		}
	});
}
/*
-------------------------------------------------
Tags Functions
-------------------------------------------------
*/
function tags_index(){
    $('#page-wrapper').load('tags/main', function(){
    	$('#tags_filter_text').bind("enterKey",function(e){
           filter_tags(1);
        });
        $('#tags_filter_text	').keyup(function(e){
            if(e.keyCode == 13)
            {
                $(this).trigger("enterKey");
            }
        });
        filter_tags(1)
    });
}

function filter_tags(page){
	var filter_text= $('#tags_filter_text').val();
	data = {filter_text: filter_text, page: page}
	$('#tags_div').load('tags/filter', data);
}

function new_tag(){
	$('#tag_form').html('');
	$('#tag_form').load('tags/new', function(){
		if($('#newTagModal')){
			$('#newTagModal').modal('show')
		}
	});
}

function create_tag(){
	var label= $('#label').val();
	var uri= $('#uri').val();
	
	data = {
		label: label, 
		uri: uri, 
	};
	$.ajax({
	    type: "POST",
	    url: "tags/create",
	    dataType: "json",
	    data: data,
	    success: function (response) {
			console.log(response.msg)
			if(response.status==1){
				$('#newTagModal').modal('hide');
				filter_tags(1);
			}else{
				$('#modal_error_msg').html(response.msg)
			}
	    },
	    error: function (request, status, err) {
	    	console.log(err);
	    }
	});
}

var typeaheadSource = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('label'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    identify: function(tag) { return tag.label; },
    local: [],
    limit: 15,
    name: 'typeaheadSource',
    ttl: 0,
    'cache': false
});
typeaheadSource.initialize(true);
$.get( "tags/list", 
    function( data ) {
        $.each(data, function(i, tag){
            typeaheadSource.add(tag);
        });
        
    }
);


var tagSuggestionTemplate= {suggestion: Handlebars.compile('<div><strong>{{label}}</strong><br>-{{uri}}</div>')};