function Events(){
    this.endpoint = 'http://localhost:9000/sparql';
    this.events = [];
    this.selector = '#result';
    this.number_events_render = 6;

    const sparqlEvents = new Sparql(this.endpoint);
    const defaultQuery = allEventsQuery;

    this.loadEvents = function (query=defaultQuery){
        this.clearEvents();
        loading(true);
        //this is a query for events
        sparqlEvents.query(query).then((response)=> this.processResponse(response))
    }

    this.processResponse = function(response){
        this.events = response;
        this.showElement("#no-result", this.events.length===0);
        this.showMore() //render the first (number_events) events in HTML, deleting the previous
        loading(false);
    }

    this.showMore = function(number_events=this.number_events_render) {
        if(this.events.length>0){
            let events_to_render = this.events.slice(0, number_events) //get a sublist of the first n(number_events) elements of events
            this.renderEvents(events_to_render)//render the events in HTML
            this.events.splice(0,number_events)//delete the fist n(number_events) elements of events from original list
        }
        this.showElement("#buttonShow", this.events.length>0);
    }

    /**
     * This function is to clear all the elements in the html
     * It is useful when we are going to do another request to the server with different filters
     */
    this.clearEvents =  function() {
        d3.select(this.selector).selectAll("*").remove();
        this.events = [];
        this.showElement("#no-result", false);
    }

        /*
    Render the list of events in HTML similar to the template
    if reset is true then previous events in DOM are deleted
     */
    this.renderEvents = function(events_list){
       /* This is the template created dinamicaly
       <div class="card-body">
            <h5 class="card-title">Las palabras desnudas</h5>
            <h6 class="card-subtitle mb-2 text-muted">Fortificación y ciudad. 29 maquetas</h6>
            <p class="card-text"><small>Un hombre vive sumido en unaprofunda crisis tras varios añosseparado de la que fue su parejasentimental. La culpa, los remordimientosy la nostalgia, le mantienensumido en un estado de ansiedadconstante que le llevará a rozar lalocura. De ese período oscuronace la necesidad de escribir undiario personal. Lo que comenzócomo un ejercicio catártico, poco apoco se va convirtiendo en laaventura más fascinante de suvida? La que le llevará a encontrarun amor que jamás había conocido. 60 minutos</small></p>
            <span class="badge bg-success">CursosTalleres</span>
            <span class="badge bg-success">Mujeres</span>
            <hr class="col-12">
            <ul class="list-group list-group-flush">
                <li class="list-group-item"><i class="bi bi-calendar-range-fill" title="Date range"></i> 2021-10-05 - 2021-10-06 </li>
                <li class="list-group-item"><i class="bi bi-calendar-x-fill" title="Excluded days"></i> 12/10/2021</li>
                <li class="list-group-item"><i class="bi bi-calendar-week-fill" title="Days"></i> M,T,W,S,F</li>
                <li class="list-group-item"><i class="bi bi-clock-fill" title="Hour"></i> 20:00:00</li>
                <li class="list-group-item"><i class="bi bi-geo-alt-fill" title="Held in"></i> Centro cultural</li>
            </ul>
            <hr class="col-12">

            <i class="bi bi-currency-euro" title="Price"></i>
            <small class="text-muted">Gratuito</small>

            <div class="card-footer text-center">
               <a class="btn btn-primary" href="http://www.madrid.es/sites/v/index.jsp?vgnextchannel=ca9671ee4a9eb410VgnVCM100000171f5a0aRCRD&amp;vgnextoid=785be0464605c710VgnVCM1000001d4a900aRCRD">Ver más</a>
            </div>
        </div>
       * */

        var eventosDiv = d3.select(this.selector, "div")
        var eventosRow = eventosDiv.append("div").attr("class", "row")
        var events = eventosRow.selectAll(".card-body")
            .data(events_list)
            .enter()
            .append("div").attr("class", "col col-xl-4 col-lg-12 col-md-12 col-sm-12")
            .append("div").attr("class", "card")
            .append("div").attr("class", "card-body")

        events.append("h5").attr("class", "card-title")
            .text(function(col) { return col.Label })
        events.append("h6").attr("class", "card-subtitle mb-2 text-muted")
            .text(function(col) { return col.Title })
       /* events.append("p").attr("class", "card-text")
            .style("height", "30vh").style("overflow", "auto")
            .append("small")
            .text(function(col) { return col.Description })
    */
        events.append("span").attr("class", "badge bg-success me-1")
            .text(function(col) { return col.Type })
        events.append("span").attr("class", "badge bg-success")
            .text(function(col) { return col.TargetAudience })

        events.append("hr").attr("class", "col-12")

        properties = events.append("ul").attr("class", "list-group list-group-flush")
        properties.append("li").attr("class", "list-group-item")
            .append("i").attr("class", "bi bi-calendar-range-fill").attr("title", "Date range")
            .text(function(col)
                {
                    var dateString = " "
                    if(col.StartDate){
                        dateString += col.StartDate.toISOString().slice(0, 10);
                        if(col.FinishDate){
                            dateString += " - " + col.FinishDate.toISOString().slice(0, 10)
                        }
                    }
                    return dateString

                })
        properties.append("li").attr("class", "list-group-item")
            .append("i").attr("class", "bi bi-calendar-x-fill").attr("title", "Excluded days")
            .text(function(col)
                {
                    if(col.ExcludedDays){
                        return " " + col.ExcludedDays.replace(/;/g," ")
                    }
                    return ""
                })

        properties.append("li").attr("class", "list-group-item")
            .append("i").attr("class", "bi bi-calendar-week-fill").attr("title", "Days")
            .text(function(col)
                {
                    if(col.Days){
                        return " " + col.Days
                    }
                    return ""
                })

        properties.append("li").attr("class", "list-group-item")
            .append("i").attr("class", "bi bi-clock-fill").attr("title", "Hour")
            .text(function(col)
                {
                    if(col.Hour){
                        return " " + col.Hour.split(":")[0]+":"+ col.Hour.split(":")[1]
                    }
                    return ""
                })

        properties.append("li").attr("class", "list-group-item")
            .append("i").attr("class", "bi bi-geo-alt-fill").attr("title", "Held in")
            .text(function(col)
                {
                    if(col.HeldIn){
                        return " " + col.HeldIn
                    }
                    return ""
                })

        events.append("hr").attr("class", "col-12")

        events.append("i").attr("class", "bi bi-currency-euro").attr("title", "Price")

        events.append("small").attr("class", "text-muted")
            .text(function(col) { return col.Price })

        events.append("div").attr("class", "card-footer text-center")
            .append("a").attr("class", "btn btn-primary")
            .attr("href", function(col) { return col.URL }).text("More details")
            .attr("target","_blank")

    }

    /**
     * To show or hide one element
     */
    this.showElement = function (idSelector, show){
        element = d3.select(idSelector);
        if (show){
             element.style('display', 'block');
        } else{
            element.style('display', 'none');
        }
    }

    /**
     * This function is for simulating that the page is loading
     * It is useful when waiting for a response
     * @param show
     */
    function loading(show=false){
        loadingElement = d3.select("#loading");
        if (show){
             loadingElement.style('display', 'block');
        } else{
            loadingElement.style('display', 'none');
        }
    }
}