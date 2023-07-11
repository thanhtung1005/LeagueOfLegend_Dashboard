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
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon update-class" data-id="${data.id}">
                            <i class="ti-pencil text-primary"></i>
                        </button>
                    </td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon delete-class" data-id="${data.id}">
                            <i class="ti-close text-danger"></i>
                        </button>
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
