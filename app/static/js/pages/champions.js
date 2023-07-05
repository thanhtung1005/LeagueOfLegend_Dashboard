(function($) {
    'use strict';
    class Champions extends BaseObject{
        constructor() {
            super({singular: 'champion', many: 'champions'}, ['blurb'], ModeImport.SingleFile);
            this.API.viewStats = `/${this.objectName}/championStats`;
            this.$inputModal = new InputChampionModal();
        }

        renderPage() {
            super.renderPage()
            this.renderUpdateObject();
            this.renderViewChampionStats()
        }

        renderViewChampionStats(){
            this.$tbody.find(`.view-champion-stats`).each((index, element) => {
                element = $(element);
                let id = element.attr('data-id');
                element.on('click', () => utils.sendRequest(
                    this.API['getOne'] + `/${id}`, null,
                    async resp => {
                        this.$showModal.show(
                            `${resp.name} - ${resp.title}`,
                            {
                                header: ["Stat", "Value"],
                                data: [
                                    ["HP", resp.statHP],
                                    ["MP", resp.statMP],
                                    ["Move speed", resp.statMoveSpeed],
                                    ["Armor", resp.statArmor],
                                    ["Attack range", resp.statAttackRange],
                                    ["Attack damage", resp.statAttackDamage],
                                    ["Attack speed", resp.statAttackSpeed]
                                ]
                            },
                            resp.blurb,
                        )
                        utils.endBusy(utils.loadingPageBusyId);
                    }
                ))
            })
        }

        renderTableData(numOrder, data) {
            this.$tbody.append(
                `
                <tr>
                    <td>${numOrder}</td>
                    <td style="text-align: center">${data.name}</td>
                    <td style="text-align: center">${data.infoAttack}</td>
                    <td style="text-align: center">${data.infoMagic}</td>
                    <td style="text-align: center">${data.infoDefense}</td>
                    <td style="text-align: center">${data.infoDifficulty}</td>
                    <td style="text-align: center">
                        <span class="view-champion-stats btn-link" data-id="${data.id}" data-name="${data.name}">View</span>
                    </td>
                    <td style="text-align: center">
                        <span class="update-champion btn-link" data-id="${data.id}" data-name="${data.name}">Update</span>
                        </br>
                        <span class="delete-champion btn-link" data-id="${data.id}" data-name="${data.name}">Delete</span>
                    </td>
                </tr>
                `
            )
        }

    }
    $(function() {
        const champions = new Champions();
        champions.init();
    })
})(jQuery);
