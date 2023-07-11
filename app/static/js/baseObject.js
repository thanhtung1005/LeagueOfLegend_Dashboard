'use strict';

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

class BaseObject {
    constructor(objectName, nullableAttr, modeImport) {
        this.objectName = objectName || {singular: 'object', many: 'objects'};
        this.nullableAttr = nullableAttr || [];
        this.modeImport = modeImport;
        this.capitalizeFirstLetterObjectName = {
            singular: capitalizeFirstLetter(this.objectName.singular),
            many: capitalizeFirstLetter(this.objectName.many)
        }
        this.prefix = `/${this.objectName.many}/`
        this.API = {
            add: `add${this.capitalizeFirstLetterObjectName.singular}`,
            delete: `delete${this.capitalizeFirstLetterObjectName.singular}`,
            deleteAll: `deleteAll${this.capitalizeFirstLetterObjectName.many}`,
            getAll: `getAll${this.capitalizeFirstLetterObjectName.many}`,
            getOne: `get${this.capitalizeFirstLetterObjectName.singular}`,
            import: `import${this.capitalizeFirstLetterObjectName.many}`,
            search: `search${this.capitalizeFirstLetterObjectName.singular}`,
            update: `update${this.capitalizeFirstLetterObjectName.singular}`,
        };
        for (let attr in this.API) {
            this.API[attr] = this.prefix + this.API[attr];
        }

        this.objectsList = null;

        this.$showModal = new ShowTableModal();

        this.modeInput = null;
        this.$inputModal = new InputDataModal();

        this.$btnCreate = $('.btn-create');
        this.$btnExport = $('.btn-export');
        this.$searchBox = $('.search-box');

        this.currentViewChampion = null;
        this.currentPage = 1;
        this.perPage = 30;

        this.$paginationGroup = $('.pagination-group');
        this.$pagination = $('.pagination');

        this.$dataTableTitle = $('.data-table-title');
        this.$dataTableTitle.text(`${this.capitalizeFirstLetterObjectName.many} List`)
        this.$table = $(`.${this.objectName.many}-table`);
        this.$tbody = this.$table.find('tbody');

        this.$buttonImport = $('.btn-import');
        this.$buttonImport.on('click', this.onClickImportBtn.bind(this));

        if (this.modeImport == ModeImport.SingleFile) {
            this.$formImport = document.getElementById('upload-data-files');
            this.$inputImport = $('#data-import-input');
            this.$inputImport.on('change', this.acceptSingleFileImport.bind(this));
        } else if (this.modeImport == ModeImport.MultiFiles) {
            this.$importModal = new MultiImportModal();
            this.$importModal.$btnImport.on('click', this.acceptMultipleFilesImport.bind(this));
        }

        this.$buttonDeleteAll = $('.btn-delete-all');
    }

    async init() {
        let requestList = [
            utils.sendRequest(this.API['getAll'], null, async resp => {
                this.objectsList = resp;
            })
        ];

        utils.startBusy();
        await Promise.all(requestList);
        this.renderPage();
        this.handleAcceptInputEvent();
        this.handleSearchEvent();
        this.handleExportEvent();
        this.handleDeleteAllEvent();
        utils.endBusy();
    }

    renderPage() {
        this.renderObjectsList(this.objectsList);
        this.renderDeleteObject();
        this.renderUpdateObject();
        this.renderAddObject();
    }

    onClickImportBtn() {
        if (this.modeImport == ModeImport.SingleFile) {
            this.$inputImport.trigger('click');
        } else if (this.modeImport == ModeImport.MultiFiles) {
            this.$importModal.show();
        }
    }

    acceptSingleFileImport() {
        utils.startBusy()
        let formData = new FormData(this.$formImport);
        utils.sendRequestFile(
            this.API['import'],
            formData,
            async resp => {
                this.handleResponseImport(resp);
                utils.endBusy();
                this.renderPage();
            },
            error => {
                utils.endBusy();
                utils.showWarn(error);
            }
        )
    }

    acceptMultipleFilesImport() {
        utils.startBusy();
        this.$importModal.hide();
        let formData = new FormData(this.$importModal.$formImport);
        utils.sendRequestFile(
            this.API['import'],
            formData,
            async resp => {
                this.handleResponseImport(resp);
                utils.endBusy();
                this.renderPage();
            },
            error => {
                utils.endBusy();
                utils.showWarn(error);
            }
        )
    }

    handleResponseImport(resp) {
        if (resp.numAdded > 0) {
            utils.showSuccess(`${resp.numAdded} of ${this.objectName.many} successfully added`);
            this.objectsList = resp.objectsList;
        } else {
            utils.showWarn(`None of ${this.objectName.many} was added`);
        }
        utils.endBusy();
        this.$showModal.show(
            `${this.capitalizeFirstLetterObjectName.many} add results`,
            {
                header: [
                    `${this.capitalizeFirstLetterObjectName.singular} name`,
                    `${this.capitalizeFirstLetterObjectName.singular} add result`
                ],
                data: resp.results,
                options: {
                    countResult: {
                        success: resp.numAdded,
                        error: resp.numFailed
                    }
                }
            },
        );
    }

    handleExportEvent() {
        this.$btnExport.on('click', () => console.log('test export'))
    }
    handleDeleteAllEvent() {
        this.$buttonDeleteAll.on('click', () => {
            utils.startBusy();
            utils.sendRequest(
                this.API['deleteAll'], null,
                async resp => {
                    utils.showSuccess(resp)
                    this.objectsList = [];
                    utils.endBusy();
                    this.renderPage();
                }
            );
        })
    }

    handleSearchEvent() {
        this.$searchBox.on('change', () => utils.sendRequest(
            this.API['search'], this.$searchBox.val(),
            async resp => {
                this.objectsList = resp;
                this.renderPage();
            }
        ));
    }

    renderObjectsList(data) {
        if (data.length != 0) this.renderPagination(data.length);
        let currentPageData = data.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage);

        let dataNum = currentPageData.length;
        let numOrder = (this.currentPage - 1) * this.perPage;

        this.$tbody.empty();
        if (this.objectsList.length == 0) {
            this.$tbody.append(`<tr><td class="text-center" colspan="99"><b>No ${this.objectName.many} data</b></td></tr>`)
        }

        for (let i = 0, n = dataNum; i < n; i++) {
            let row = currentPageData[i];
            this.renderTableData(numOrder + 1, row);
            numOrder++;
        }
        this.$paginationGroup.removeClass("d-none");
    }

    renderTableData(numOrder, data) {
    }

    renderAddObject() {
        this.$btnCreate.on('click', () => {
            this.$inputModal.onChangeInput(true);
            this.modeInput = ModeInput.Create;
            this.$inputModal.API = this.API['add'];
            this.$inputModal.$title.text(`Add new ${this.objectName.singular}`);
            this.$inputModal.clearForm();
            this.$inputModal.show();
        })
    }
    renderUpdateObject() {
        this.$tbody.find(`.update-${this.objectName.singular}`).each((index, element) => {
            element = $(element);
            let id = element.attr('data-id');
            element.on('click', () => utils.sendRequest(
                this.API['getOne'] + `/${id}`, null,
                async resp => {
                    this.$inputModal.$title.text(`Update ${this.objectName.singular} ${resp.name}`);
                    for (let attr in resp){
                        if (attr != 'id') {
                            this.$inputModal.$inputData[attr].val(resp[attr]);
                        }
                    }
                    this.modeInput = ModeInput.Update;
                    this.$inputModal.API = this.API['update'] + `/${id}`;
                    this.$inputModal.show();
                }
            ))
        })
    }

    handleAcceptInputEvent() {
        this.$inputModal.$form.on('change', () => {
            if (this.modeInput == ModeInput.Update) {
                this.$inputModal.onChangeInput(false)
            } else if (this.modeInput == ModeInput.Create) {
                let data = this.$inputModal.getData();
                let disableAccept = false;
                for (let attr in data) {
                    if (this.nullableAttr.includes(attr)) continue;
                    if (!data[attr]) {
                        disableAccept = true;
                        break;
                    }
                }
                this.$inputModal.onChangeInput(disableAccept);
            } else {
                throw new Error(`Invalid mode input ${this.modeInput}`);
            }
        });
        this.$inputModal.$btnConfirm.on('click', () => {
            if (this.modeInput == ModeInput.Update) {
                this.handleAcceptUpdateEvent();
            } else if (this.modeInput == ModeInput.Create) {
                this.handleAcceptCreateEvent();
            } else {
                throw new Error(`Invalid mode input ${this.modeInput}`);
            }
            this.$inputModal.onChangeInput(true);
        })
    }

    handleAcceptUpdateEvent() {
        let data = this.$inputModal.getData();
        utils.startBusy();
        utils.sendRequest(this.$inputModal.API, data, resp => {
            utils.endBusy();
            utils.showSuccess(resp.message);
            for (let i = 0; i < this.objectsList.length; i++) {
                if (this.objectsList[i].id != resp.id) continue;
                else {
                    for (let attr in resp) {
                        if (attr == 'message' || attr == 'id') continue;
                        this.objectsList[i][attr] = resp[attr];
                    }
                }
            }
            this.$inputModal.$modal.modal('hide');
            this.renderPage();
        })
    }

    handleAcceptCreateEvent() {
        let data = this.$inputModal.getData();
        utils.startBusy();
        utils.sendRequest(this.$inputModal.API, data, resp => {
            utils.endBusy();
            utils.showSuccess(`Succesfully add new ${this.objectName.singular} ${data.name}.`);
            this.$inputModal.$modal.modal('hide');
            this.objectsList = resp;
            this.renderPage();
        })
    }

    renderDeleteObject(){
        this.$tbody.find(`.delete-${this.objectName.singular}`).each((index, element) => {
            element = $(element);
            let id = element.attr('data-id');
            element.on('click', () => utils.sendRequest(
                this.API['delete'] + `/${id}`, null,
                async resp => {
                    this.objectsList = this.objectsList.filter((item) => {
                        return item.id != resp.id
                    })
                    utils.showSuccess(`Successfully delete ${resp.name}.`);
                    this.renderPage();
                }
            ))
        })
    }

    renderPagination(totalData){
        if(Math.floor(totalData/this.perPage) < this.currentPage){
            this.currentPage = Math.max(Math.ceil(totalData / this.perPage), 1);
        }

        this.$pagination.pagination({
            items: totalData,
            itemsOnPage: this.perPage,
            currentPage: this.currentPage,
            onPageClick: this.onClickPage.bind(this)
        })
    }

    onClickPage(pageNum){
        this.currentPage = pageNum;
        this.renderPage();
    }
}
