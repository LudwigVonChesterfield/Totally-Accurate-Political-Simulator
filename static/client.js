/*
const keyEvent2JSON = (e) =>
{
	var keyEvent = {};
	keyEvent.keyCode = e.keyCode;
	/*
	for(var key in e)
	{
		// We can't pass object references.
		if(typeof e[key] === 'object' && e[key] !== null)
		{
			continue;
		}
		keyEvent[key] = e[key];
	}
	*\/
	return JSON.stringify(keyEvent);
}
*/

const writeEvent = (text, to_event) => {
	// <ul> element.
	const parent = document.querySelector(to_event);

	// <li> element appending to the <ul> abovve.
	const el = document.createElement('li');
	el.innerHTML = text;

	var updateScroll = false;

	// Scroll so the newest message is visible, unless client themselves scrolled up. 10 is const IMPORTANT_MAGICAL_SCROLLBAR_CONSTANT = 10; in disguise.
    // It's actually the message padding pixel height.
	if(parent.scrollTop + parent.clientHeight + el.scrollHeight + 10 >= parent.scrollHeight)
	{
		updateScroll = true;
	}

	parent.appendChild(el);

	if(updateScroll)
	{
		parent.scrollTop = parent.scrollHeight;
	}
};

const onFormSubmitted = (e, entity) => {
	e.preventDefault();

    const input = document.querySelector("#" + entity + "_chat");
	const text = input.value;

	if(text == "")
	{
		writeEvent("Your message is empty.", "#" + entity + "_events")
		return;
	}

	if(text.length > 256)
	{
		writeEvent("Your message is too long.", "#" + entity + "_events")
		return;
	}

	input.value = '';
    input.focus();

	socket.emit(entity + "_message", {data: text});
};

// writeEvent('Welcome to Totally Accurate Political Simulator.', "#npc_events");

const socket = io();

/*
socket.on('connect', function()
{
	var form = $('form').on('submit', function(e)
	{
		e.preventDefault()
		let user_name = $( 'input.username' ).val()
		let user_input = $( 'input.message' ).val()

		socket.emit('my event',
		{
			user_name : user_name,
			message : user_input
		})
	$('input.message').val( '' ).focus()
	})
})
*/

socket.on('npc_message', (json) => {
	writeEvent(json.data, "#npc_events");
});

socket.on('player_message', (json) => {
    writeEvent(json.data, "#player_events");
});

/*
window.addEventListener("keydown", (e) =>
{
	var keyEvent = keyEvent2JSON(e);
	socket.emit('keyDown', keyEvent);
});

window.addEventListener("keyup", (e) =>
{
	var keyEvent = keyEvent2JSON(e);
	socket.emit('keyUp', keyEvent);
});
*/

window.onload = function()
{
	document
		.querySelector('#npc_chat-form')
		.addEventListener('submit', function(e)
            {
                onFormSubmitted(e, "npc")
            });

    /*
    document
        .querySelector('#player_chat-form')
        .addEventListener('submit', function(e)
            {
                onFormSubmitted(e, "player")
            });
    */
};
