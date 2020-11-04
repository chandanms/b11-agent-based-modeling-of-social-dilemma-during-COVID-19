var TextDisplay = function() {
	
	// Create the tag:
    var canvas_tag = '<div style="position: relative; top: 10px; left: 100px"><ul class="legend" style="list-style-type:none;"><li style="float: left; margin-right: 10px;"><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color: #00008b;"></span>Clean</li><li style="float: left; margin-right: 10px;"><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; background-color: #FF0000; "></span>Infected</li><li style="float: left; margin-right: 10px;"><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px;background-color: #FFA500; "></span>Quarantine</li><li><span style="border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px;background-color: #008000; "></span> Recovered</li></ul></div>';
    
	// Append it to #elements
    $("#elements").append(canvas_tag);
	
	// Render canvas with updated data
    this.render = function(data) {
	$(canvas_tag).html(data);
	};
	
	// Reset canvas
	this.reset = function() {
	$(canvas_tag).html("");
	};
	
}
