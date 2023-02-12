$(document).ready(function (e) {
        
        

    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: '/list_event',
        selectable: true,
        selectHelper: true,
        editable: true,
        eventLimit: true,
        droppable: true,
        drop: function(date) {
            var now = new moment();

            let startdate = date.format("Y-MM-DD");
            let starttime = now.format("HH:mm");
            let enddate =  date.format("Y-MM-DD");
            let endtime = now.format("HH:mm");
            
            $.ajax({
                type: "GET",
                url: 'updatedrag/',
                data: { 
                            

                        'start-date':startdate,
                        'end-date':enddate,
                        'start-time': starttime, 
                        'end-time': endtime, 
                        
                    },
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    
                },
                error: function (data) {
                    console.log('There is a problem!!!');
                }
            });
          },
        // start the select event
        eventClick: function(event) {
           let startdate = $.fullCalendar.formatDate(event.start, "Y-MM-DD");
           let starttime = $.fullCalendar.formatDate(event.start, "HH:mm");
           let enddate = $.fullCalendar.formatDate(event.end, "Y-MM-DD");
           let endtime = $.fullCalendar.formatDate(event.end, "HH:mm");

            Swal.fire({title: event.title, 
            html: '<div class="event-details">'+
                '<div class="d-flex mb-2">'+'<div class="flex-grow-1">'+
                '<p> Date :  <span class="fw-semibold">'+startdate+' To '+enddate+'</span></p>'+
                       
                    '</div></div>'+'<div class="flex-grow-1">'+
                        '<h6 class="d-block fw-semibold mb-0"> Time : <span>'+starttime+' To '+endtime+'</span></h6>'+
                    '</div>'+
                    '</div></div>'+'<div class="flex-grow-1">'+
                        '<h6 class="d-block fw-semibold mb-0"> Event owner : <span>'+event.owner+'</span></h6>'+
                    '</div>'+
                    '<div class="flex-grow-1">'+
                       ' <h6 class="d-block fw-semibold mb-0"> <span id="event-location-tag">Location: <span>'+event.location+'</span></span></h6>'+
                    '</div><div class="flex-grow-1">'+
                       ' <p class="d-block text-muted mb-0" id="event-description-tag">'+event.description+'</p>'+
                    '</div>',

                    showCancelButton: true,
                    showDenyButton: true,
                    showCancelButton: true,
                    confirmButtonText: 'delete',
                    confirmButtonColor: "#DD6B55",
                    denyButtonColor: '#8CD4F5',
                    denyButtonText: 'update',

                    }).then((result) => {       
                        if(result.isConfirmed){
                        $.ajax({
                            type: "POST",
                            url: "/delete_event",
                            data: { event_id: event.id,
                                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()

                            },
                            cache: false,
                            success: function(response) {
                                Swal.fire(
                                "Sccess!",
                                "Your was delete!",
                                "success"
                                )
                                calendar.fullCalendar('refetchEvents');
                            },
                            failure: function (response) {
                                Swal.fire(
                                "Internal Error",
                                "Oops, your note was not saved.", // had a missing comma
                                "error"
                                )
                            }
                        });

                    } else if(result.isDenied){

                        $('#update-event').find('input[name=category]').val(event.color);
                        $('#update-event').find('input[name=title]').val(event.title);
                        $('#update-event').find('input[name=start-date]').val(startdate);
                        $('#update-event').find('input[name=end-date]').val(enddate);
                        $('#update-event').find('input[name=start-time]').val(starttime);
                        $('#update-event').find('input[name=end-time]').val(endtime);
                        $('#update-event').find('input[name=event-location]').val(event.location);                        $('#up-description').val(event.description)
                        $('#event-update-modal').modal("show");
                        $('#update-event').submit(function(e) {
                            
                            $.ajax({
                              url: 'update_event/'+event.id+'/',
                              type: 'POST',
                              data: $(this).serialize(),
                              success: function(response) {

                                console.log(response.message);
                                calendar.fullCalendar('refetchEvents');
                              },
                              error: function(response) {
                                console.error(response.message);
                              }
                            });
                        });



                    }
                    
                })},

                eventDrop: function (event) {
                    let startdate = $.fullCalendar.formatDate(event.start, "Y-MM-DD");
                    let starttime = $.fullCalendar.formatDate(event.start, "HH:mm");
                    let enddate = $.fullCalendar.formatDate(event.end, "Y-MM-DD");
                    let endtime = $.fullCalendar.formatDate(event.end, "HH:mm");
                    let id = event.id
                    $.ajax({
                        type: "GET",
                        url: 'updatedrop/',
                        data: { 
                                    
    
                                'start-date':startdate,
                                'end-date':enddate,
                                'start-time': starttime, 
                                'end-time': endtime, 
                                'id': id,
                            },
                        dataType: "json",
                        success: function (data) {
                            calendar.fullCalendar('refetchEvents');
                            
                        },
                        error: function (data) {
                            console.log('There is a problem!!!');
                        }
                    });
                }

                // End Select Event
                
        

        
          })
    })
    

$(document).on('submit', '#form-event',function(e){
    
    $.ajax({
        type:'POST',
        url : 'add_event/',
        
        data:{
            
            event_cat:$('#event-category').val(),
            title:$('#event-title').val(),
            start_date:$('#event-start-date').val(),
            end_date:$('#event-end-date').val(),
            start_time:$('#start-time').val(),
            end_time:$('#end-time').val(),
            location:$('#event-location').val(),
            description:$('#event-description').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action:'post'
            },
        

        success:function(json){
            
            
            calendar.fullCalendar('refetchEvents');
            },
        error:function(xhr,errmsg,err){
                console.log(xhr.status + ": " + xhr.responseText);
            }
    });
    
});