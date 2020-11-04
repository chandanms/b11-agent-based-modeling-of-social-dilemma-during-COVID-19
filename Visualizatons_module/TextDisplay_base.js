var TextDisplay = function() {
    var canvas_tag = '<div style="position: relative; top: 10px; left: 100px"><ul class="legend" style="list-style-type:none;"><li style="float: left; margin-right: 10px;"><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color: #00008b;"></span>Clean</li><li style="float: left; margin-right: 10px;"><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color: #FF0000; "></span>Infected</li><li style="float: left; margin-right: 10px;"><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px;background-color: #FFA500; "></span>Quarantine</li><li><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px;background-color: #008000; "></span> Recovered</li></ul></div>';
    // Append it to #elements
    //var canvas = $(canvas_tag)[0];
    $("#elements").append(canvas_tag);
    this.render = function(data) {
	$(canvas_tag).html(data);
	};

	this.reset = function() {
	$(canvas_tag).html("");
	};
	
}
