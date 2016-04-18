var timeout= 5 * 60 * 1000;

function info_index(){
    $('#page-wrapper').load('info/main');
}

function lessons_index(){
    $('#page-wrapper').load('lessons/main', function(){
        filter_lessons(1)
    });
}

function filter_lessons(page){
	var filter_type= $('#filter_type').val();
	var filter_text= $('#search_field').val();
	data = {filter_type: filter_type, filter_text: filter_text, page: page}
	$('#lessons_div').load('lessons/filter', data);
}

function new_lesson(){
	$('#lesson_form').html('');
	$('#lesson_form').load('lessons/new', function(){
		if($('#newLessonModal')){
			$('#newLessonModal').modal('show')
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
				$('#newLessonModal').modal('hide');
				filter_lessons(1);
			}

	    },
	    error: function (request, status, err) {
	    	alert(err);
	    }
	});
}

/*
function question_detail(question_id, ner_id){
    $('#page-wrapper').load('question/detail/'+ question_id+"/"+ ner_id);
}

function refresh_question_info(question_id, ner_id){
    $('#question_info').load('question/detail/info/'+ question_id+"/"+ ner_id);
}
v
function load_resource_info(uri){
	console.log(uri)
	$('#resource_info_modal_content').html('');
	$('#resource_info_modal_content').load('resource/info/'+ uri, function(){
		if($('#myModal')){
			$('#myModal').modal('show')
		}
	});
}

*/