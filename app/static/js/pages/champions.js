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
                        utils.endBusy();
                    }
                ))
            })
        }

        renderTableData(numOrder, data) {
            this.$tbody.append(
                `
                <tr>
                    <td>${numOrder}</td>
                    <td>${data.name}</td>
                    <td>${data.classes}</td>
                    <td>${data.roles}</td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon view-champion-infor" data-id="${data.id}">
                            <i class="ti-eye text-info"></i>
                        </button>
                    </td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon view-champion-stats" data-id="${data.id}">
                            <i class="ti-eye text-info"></i>
                        </button>
                    </td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon update-champion" data-id="${data.id}">
                            <i class="ti-pencil text-primary"></i>
                        </button>
                    </td>
                    <td style="text-align: center">
                        <button type="button" class="btn btn-outline-secondary btn-rounded btn-icon delete-champion" data-id="${data.id}">
                            <i class="ti-close text-danger"></i>
                        </button>
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
