(function($) {
    'use strict';
    class Home {

        constructor() {
            this.API = {
                getAllChampionsInfor: 'champions/getAllChampionsInfor',
                getAllItemsPrice: 'items/getAllItemsPrice',
                getTotalRoles: 'roles/getTotalRoles',
                getTotalClasses: 'classes/getTotalClasses',
            };
            this.STATISTICS_API = {

            }
            this.$totalChampions = $('#total-champions');
            this.$totalItems = $('#total-items');
            this.$totalClasses = $('#total-classes');
            this.$totalRoles = $('#total-roles');

            this.$championsAttackChart = $('#champions-attack-chart');
            this.$championsMagicChart = $('#champions-magic-chart');
            this.$championsDefenseChart = $('#champions-defense-chart');
            this.$championsDifficultyChart = $('#champions-difficulty-chart');

            this.$itemsBuyPriceChart = $('#items-buy-price-chart');
            this.$itemsSellPriceChart = $('#items-sell-price-chart');
        }

        async init() {
            let requestsList = [
                utils.sendRequest(this.API.getAllChampionsInfor, null, async resp => {
                    this.$totalChampions.text(resp.total);
                    if (resp.total) this.drawChampionsInforChart(resp);
                }),
                utils.sendRequest(this.API.getAllItemsPrice, null, async resp => {
                    this.$totalItems.text(resp.total);
                    if (resp.total) this.drawItemPriceChart(resp);
                }),
                utils.sendRequest(this.API.getTotalClasses, null, async resp => {
                    this.$totalClasses.text(resp);
                }),
                utils.sendRequest(this.API.getTotalRoles, null, async resp => {
                    this.$totalRoles.text(resp);
                }),
            ]
            utils.startBusy(utils.loadingPageBusyId);
            await Promise.all(requestsList);
            utils.endBusy(utils.loadingPageBusyId);
        }

        drawChampionsInforChart(championsData) {
            let options = {
                scales: {x: {ticks: {display: false}}}
            }
            DrawCharts.drawSingleChart(
                this.$championsAttackChart,
                'line', championsData.name,
                championsData.infoAttack,
                'Attack', 'rgba(75, 73, 172, 0.7)',
                'Attack of champions',
                `mean: ${Utils.average(championsData.infoAttack).toFixed(2)}`, options
            )

            DrawCharts.drawSingleChart(
                this.$championsMagicChart,
                'line', championsData.name,
                championsData.infoMagic,
                'Magic', 'rgba(243, 121, 126, 0.7)',
                'Magic of champions',
                `mean: ${Utils.average(championsData.infoMagic).toFixed(2)}`, options
            )

            DrawCharts.drawSingleChart(
                this.$championsDefenseChart,
                'line', championsData.name,
                championsData.infoDefense,
                'Defense', 'rgba(87, 182, 87, 0.7)',
                'Defense of champions',
                `mean: ${Utils.average(championsData.infoDefense).toFixed(2)}`, options
            )

            DrawCharts.drawSingleChart(
                this.$championsDifficultyChart,
                'line', championsData.name,
                championsData.infoDifficulty,
                'Difficulty', 'rgb(87, 199, 212, 0.7)',
                'Difficulty of champions',
                `mean: ${Utils.average(championsData.infoDifficulty).toFixed(2)}`, options
            )
        }

        drawItemPriceChart(itemData) {
            let options = {
                scales: {x: {ticks: {display: false}}}
            }
            DrawCharts.drawSingleChart(
                this.$itemsBuyPriceChart,
                'line', itemData.name,
                itemData.buyPrice,
                'Buy price', 'rgba(75, 73, 172, 0.7)',
                'Buy price of items',
                `mean: ${Utils.average(itemData.buyPrice).toFixed(2)}`, options
            )

            DrawCharts.drawSingleChart(
                this.$itemsSellPriceChart,
                'line', itemData.name,
                itemData.sellPrice,
                'Sell price', 'rgba(243, 121, 126, 0.7)',
                'Sell price of Items',
                `mean: ${Utils.average(itemData.sellPrice).toFixed(2)}`, options
            )
        }
    }

    $(function() {
        const home = new Home();
        home.init();
    })

})(jQuery);
