(function($) {
    'use strict';
    class Classes extends BaseObject{
        constructor() {
            super({singular: 'class', many: 'classes'}, [], ModeImport.SingleFile);
            this.$inputModal = new InputClassModal();
        }

        renderTableData(numOrder, data) {
            this.$tbody.append(
                `
                <tr>
                    <td>${numOrder}</td>
                    <td>${data.name}</td>
                    <td style="text-align: center">
                        <span class="update-class btn-link" data-id="${data.id}" data-name="${data.name}">Update</span>
                        </br>
                        <span class="delete-class btn-link" data-id="${data.id}" data-name="${data.name}">Delete</span>
                    </td>
                </tr>
                `
            )
        }

    }
    $(function() {
        const classes = new Classes();
        classes.init();
    })
})(jQuery);
