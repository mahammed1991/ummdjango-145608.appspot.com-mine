$(".sbtn").click(function (e){
	e.preventDefault();
	var checked_task = [];
	var result =[];
	var check_boxes = $(".task");
	var task = $(".task_name");
	for(var  i=0;i<check_boxes.length;i++)
	{
		if ($(check_boxes[i]).is(':checked') == true)
		{
			checked_task.push($(task[i]).attr('id'));
		}
	}	
	if (checked_task.length >0)
	{	
		var k = 1;
		$(".taskrecommend").css("opacity",0);
		$(".taskrecommend").css("height","auto");
		$(".taskrecommend2").css("opacity",0);
		$(".taskrecommend2").css("height","auto");
		$(".taskrecommend").html('');
		$(".taskrecommend2").html('<p>More Recommendations:</p>');
		$(".advertiser-goal").html('');
		for(var j=0;j<checked_task.length;j++ )
		{
			if (checked_task[j] != undefined)
			{
				$.ajax({
				    url: "/task/" + checked_task[j],
				    type: "GET",
				    datatype: "json",
				    success: function(data, response, xhr){
				    	if (data['goals'])
				    	{
						    for (var i =0;i<data['goals'].length;i++)
					    	{
					    		$(".taskrecommend").prepend('<a class="sub-task-link " parent='+  data['goals'][i]['parent_id'] +' id="'+ data['goals'][i]['id'] +'">'+ data['goals'][i]['name'] +'</a>');
					    	}
					    	$(".sub-task-link").click(function (e){
					    		localStorage.setItem("id",$(this).attr('id'));
					    		localStorage.setItem("parent_id",$(this).attr('parent'));
					    		window.open("/umm");
					    	});
				    	}
				    	$(".sub-task-link").click(function (e){
				    		localStorage.setItem("id",$(this).attr('id'));
				    		localStorage.setItem("parent_id",$(this).attr('parent'));
				    		window.open("/umm");
				    	});
				    	if (data['extra_tasks'].length > 0)
				    	{

					    	for (var i =0;i<data['extra_tasks'].length;i++)
					    	{
					    		$(".taskrecommend2").append('<ul class="extra"><li>' + data['extra_tasks'][i] + '</li></ul>');
					    	}
				    	}

				    	for (var i =0;i<data['questions'].length;i++)
				    	{
				    		$(".advertiser-goal").append('<ol start="'+ k +'" class="extra"><li>' + data['questions'][i] + '</li></ol>');
				    		k++;
				    	} 
					},

					error:function(response){
						console.log("Error");
						console.log(response);
					}
				});
			}
		}
	}
	setTimeout(function(){
	var questions = $(".advertiser-goal").children()
	for(var i=0;i<questions.length;i++)
	{
		if($(questions[i]).attr('class') == "extra")
		{
			$("h4").remove();
		}
	}
	if(questions.length ==0)
	{
		$(".advertiser-goal").html('');
		$(".advertiser-goal").append('<h4 class="text-center"> <em class="text-danger"><br>Watch out this space for your advertiser goal better<br><br></em> </h4>');
	}

	}, 300);
	setTimeout(function(){
		var seen = {};
		$('.sub-task-link ').each(function() {
		    var txt = $(this).text();
		    if (seen[txt])
		        $(this).remove();
		    else
		        seen[txt] = true;
		});
		var children_1= $(".taskrecommend").children();
		var children_2= $(".taskrecommend2").children();
		if (children_1.length == 0 & children_2.length ==1 )
		{
			$(".taskrecommend").append('<h4 class="text-center"> <em class="text-danger"><br>Watch out this space for your task recommendations<br><br></em> </h4>');
			$(".taskrecommend2").html('');
		}
		$(".taskrecommend").css("opacity",1);
		$(".taskrecommend2").css("opacity",1);
	}, 300);
});

$(".refresh").click(function (e){
	location.reload();
});