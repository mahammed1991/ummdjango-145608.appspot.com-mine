$(".sbtn").click(function (e){
	e.preventDefault();
	var checked = [];
	var result =[];
	var check_boxes = $(".task");
	var task = $(".task_name");
	for(var  i=0;i<check_boxes.length;i++)
	{
		if ($(check_boxes[i]).is(':checked') == true)
		{
			checked[i] = $(task[i]).html();
		}
	}	
	$(".taskrecommend").html('');
	$(".taskrecommend2").html('');
	$(".advertiser-goal").html('');
	if (checked.length >0)
	{	var k = 1;
		for(var j=0;j<checked.length;j++ )
		{
			if (checked[j] != undefined)
			{
				var data_sent = {"data":checked[j]}
				$.ajax({
				    url: "/task/",
				    type: "GET",
				    datatype: "json",
				    data : data_sent,
				    success: function(data, response, xhr){
				    	console.log(data);
					    for (var i =0;i<data['goals'].length;i++)
				    	{
				    		$(".taskrecommend").append('<a class="sub-task-link " href="/" >'+ data['goals'][i] +'</a>');
				    	}
				    	if(data['extra_tasks'].length > 0)
				    	{
				    		$(".taskrecommend2").html('<br><br><br><p>More Recommendations:</p>');
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
	else
	{
		$(".taskrecommend").append('<h4 class="text-center"> <em class="text-danger"><br>Watch out this space for your task recommendations<br><br></em> </h4>');
		$(".taskrecommend2").html('');
		$(".advertiser-goal").append('<h4 class="text-center"> <em class="text-danger"><br>Watch out this space for your advertiser goal better<br><br></em> </h4>');
	}
	setTimeout(function(){
		var questions = $(".advertiser-goal").children();
		console.log(questions);
		for(var i=0;i<questions.length;i++)
		{
			if($(questions[i]).attr('class') == "extra")
			{
				$("h4").remove();
			}
		}
		if(questions.length ==0)
		{
			$(".advertiser-goal").append('<h4 class="text-center"> <em class="text-danger"><br>Watch out this space for your task recommendations<br><br></em> </h4>');
		}
	}, 300);
});

