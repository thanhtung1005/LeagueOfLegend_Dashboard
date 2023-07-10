(function($) {
    'use strict';

    class Items extends BaseObject {
        constructor() {
            super({singular: 'item', many: 'items'}, ['tag', 'explain'], ModeImport.SingleFile);
            this.API.viewExplain = `/${this.objectName}/itemExplain`;
            this.$inputModal = new InputItemModal();
        }

        renderPage() {
            super.renderPage()
            this.renderViewItemExplain()
        }

        renderTableData(numOrder, data) {
            this.$tbody.append(
                `
                <tr>
                    <td>${numOrder}</td>
                    <td>${data.name}</td>
                    <td>${data.tag}</td>
                    <td style="text-align: center">
                        <span class="view-item-explain btn-link" data-id="${data.id}" data-name="${data.name}">View</span>
                    </td>
                    <td style="text-align: center">
                        <span class="update-item btn-link" data-id="${data.id}" data-name="${data.name}">Update</span>
                        </br>
                        <span class="delete-item btn-link" data-id="${data.id}" data-name="${data.name}">Delete</span>
                    </td>
                </tr>
                `
            )
        }

        renderViewItemExplain(){
            this.$tbody.find(`.view-item-explain`).each((index, element) => {
                element = $(element);
                let id = element.attr('data-id');
                element.on('click', () => utils.sendRequest(
                    this.API['getOne'] + `/${id}`, null,
                    async resp => {
                        this.$showModal.show(
                            `${resp.name}`,
                            {
                                header: ["Stat", "Value"],
                                data: [
                                    ["Buy price", resp.buyPrice],
                                    ["Sell price", resp.sellPrice],
                                    ["Tag", resp.tag],
                                ]
                            },
                            resp.explain,
                        )
                        utils.endBusy();
                    }
                ))
            })
        }
    }

    $(function() {
        const items = new Items();
        items.init();
    })
})(jQuery);
