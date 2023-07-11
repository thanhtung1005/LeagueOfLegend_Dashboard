(function($) {
    'use strict';
    class Roles extends BaseObject{
        constructor() {
            super({singular: 'role', many: 'roles'}, [], ModeImport.SingleFile);
            this.$inputModal = new InputRoleModal();
        }

        renderTableData(numOrder, data) {
            this.$tbody.append(
                `
                <tr>
                    <td>${numOrder}</td>
                    <td>${data.name}</td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon update-role" data-id="${data.id}">
                            <i class="ti-pencil text-primary"></i>
                        </button>
                    </td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon delete-role" data-id="${data.id}">
                            <i class="ti-close text-danger"></i>
                        </button>
                    </td>
                </tr>
                `
            )
        }

    }
    $(function() {
        const roles = new Roles();
        roles.init();
    })
})(jQuery);
