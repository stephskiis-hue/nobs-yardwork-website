( function( api ) {

	// Extends our custom "lawn-gardner" section.
	api.sectionConstructor['lawn-gardner'] = api.Section.extend( {

		// No events for this type of section.
		attachEvents: function () {},

		// Always make the section active.
		isContextuallyActive: function () {
			return true;
		}
	} );

} )( wp.customize );