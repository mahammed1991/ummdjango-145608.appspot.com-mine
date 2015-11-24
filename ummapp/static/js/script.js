
$(document).ready(function(){

    BudgetBandTableLoad()
    
    comboData()

    elem_id = $('ul.main-option li:first-child a').attr('id');
    taskList(elem_id);

    $('a.main-category').click(function () {
        taskList(this.id)
    });

    
});


function comboData(){
$.ajax({
        type: 'GET',
        url: '/combodata/',
        dataType: 'json',
        success: function(data, response, xhr)
        {
           
            for(i=0; i<data.length; i++)
            {
                mytag=document.createElement('a');
                mytag.setAttribute('id',data[i].pk);
                mytag.innerHTML = data[i].fields.title;
                $('.myclass').append(mytag);      
            }
            

            $('.myclass').click(function(){
                $('.mytable').empty();
                for(i=0; i<data.length; i++)
                {
                    tablerow = document.createElement('tr');
                    tablerow.setAttribute('class',"myrow" + i);
                    $('.mytable').append(tablerow);
                    newlink1=document.createElement('td');
                    newlink1.innerHTML = data[i].fields.title
                    $('.myrow' + i).append(newlink1)
                    newlink2=document.createElement('td');
                    newlink2.innerHTML = data[i].fields.description
                    $('.myrow'+ i).append(newlink2)
                }
            });
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function taskList(id){
    $.ajax({
        type: 'GET',
        url: '/task_list/'+ id ,
        dataType: 'json',
        success: function(data, response, xhr)
        {

            createSubTasks(data)
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function createSubTasks(data){
    global_id = null;
    $('.sub-task-link').remove()
    $('#key_data').remove()
    $('#value_data').remove()
    $('#key_row').empty()
    $('#value_row').empty()
    if(data!= null)
    {
        html = null
        global_id = data[0].pk
        for(i=0; i<data.length; i++)
        {
            newlink=document.createElement('a');
            newlink.setAttribute('class',"sub-task-link")
            link = data[i].pk
            newlink.setAttribute('id',link);
            newlink.innerHTML = data[i].fields.task_name;
            $('.sub-task').append(newlink);
        }
        
        TableLoad(global_id);
        PitchDataLoad(global_id);
        RightTableLoad(global_id);
    }

    $('.sub-task-link').bind('click', function(event) {
        TableLoad(event.target.id)
        PitchDataLoad(event.target.id)
        RightTableLoad(event.target.id)

    });
}

function TableLoad(taskid){
    $('#key_row').empty()
    $('#value_row').empty()
    $.ajax({
        type: 'GET',
        url: '/left_column_list/'+ taskid ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            if(data!= null)
            {
                for(i=0; i<data.length; i++)
                {
                    newlink1=document.createElement('th');
                    newlink1.innerHTML = data[i].fields.column_name
                    $('#key_row').append(newlink1)
                    newlink2=document.createElement('td');
                    newlink2.innerHTML = data[i].fields.column_value
                    $('#value_row').append(newlink2)
                }
            }
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function PitchDataLoad(taskid){
    $('#elevator_data').empty()
    
    $.ajax({
        type: 'GET',
        url: '/elevator_pitch_data/'+ taskid ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            
            $('#elevator_data').append(data[0].fields.elevator_pitch)
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function RightTableLoad(taskid){ 

    $.ajax({
        type: 'GET',
        url: '/right_column_list/'+ taskid ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            $('.tab-pane').text('');
            $('.modal-body #tab1').append(data[0].fields.email_pitch_guidelines)
            $('.modal-body #tab2').append(data[0].fields.implementation_guide)
            $('.modal-body #tab3').append(data[0].fields.faq)

            // $('ul.nav.nav-tabs li:nth-child(1)').tab('show')
            // $('ul.nav.nav-tabs li:nth-child(1)').addClass('active');
            // $('#tab1').addClass('active');

            $('a#email_pitch').click(function(){
                $('#tab2').removeClass('active');
                $('#tab3').removeClass('active');
                 $('#tab1').addClass('active');
                $('ul.nav.nav-tabs li:nth-child(3)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(2)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(1)').addClass('active');
            });
            $('a#implementation').click(function(){
                $('#tab1').removeClass('active');
                $('#tab3').removeClass('active');
                $('#tab2').addClass('active');
                $('ul.nav.nav-tabs li:nth-child(1)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(3)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(2)').addClass('active');
            });

            $('a#faq').click(function(){
                
                 $('#tab1').removeClass('active');
                  $('#tab2').removeClass('active');
                  $('#tab3').addClass('active');

                $('ul.nav.nav-tabs li:nth-child(1)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(2)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(3)').addClass('active');
            });
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function BudgetBandTableLoad(){ 
    $.ajax({
        type: 'GET',
        url: '/budget_band/',
        dataType: 'json',
        success: function(data, response, xhr)
        {
            $('a#budget_band').click(function(){
                $('.modal-body .budget-body').empty();
                $('.budget-body').append(data[0].fields.band_details)
            }); 
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}
