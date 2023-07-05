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
                        <span class="delete-role btn-link" data-id="${data.id}" data-name="${data.name}">Delete</span>
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
