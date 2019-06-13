$().ready(function () {

    $('#createWallet-btn').click(function () {
        nextStep(1);            
        $('#wallet-modal .modal-title').text('Create Wallet');        
        $('#wallet-modal .modal-footer .btn:first-child').text("Create");
        $('#wallet-modal').modal('show');
    })
    $('#searchWallet-btn').click(function () {
        $('#wallet-modal .modal-footer').removeClass('hidden');
        $('#wallet-modal .modal-title').text('Search Wallet');
        $('#wallet-modal .modal-body').html('<p>Wallet private key</p><input id="walletPrivateKey" class="form-control" type="password" placeholder="Enter Wallet Private KEY">');
        $('#wallet-modal .modal-footer .btn:first-child').text("Search");
        $('#wallet-modal').modal('show');
    })
    $('#wallet-modal').on('hide.bs.modal', function(){
        post_fetch("/wallet/create/close","{}");
    })

    $('.modal-footer .btn:first-child').click(function () {
        if ($('#wallet-modal .modal-title').text() === "Create Wallet") {
            $('#wallet-modal-confirm').removeClass('hidden');
            post_fetch('/wallet/create/', '{"wallet_name":"test_name","wallet_password":"1234"}').then(data => {
                console.log(data);
                $('#wallet-modal-confirm').addClass('hidden');
                $('#wallet-modal .modal-footer').addClass('hidden');
                $('#wallet-modal .modal-body .right-content').html('<p>Wallet Address - <strong>' + data.address + '</strong> </p>'
                    + '<p>Wallet private Key - <strong>' + data.private_key + '</strong> </p>');
            });
        }
        if ($('#wallet-modal .modal-title').text() === "Search Wallet") {
            $('#wallet-modal-confirm').removeClass('hidden');
            post_fetch('/wallet/search/', '{"private_key":"' + $('#walletPrivateKey').val() + '"}').then(data => {
                if (data === "fail") {
                    $('#wallet-modal').modal('hide');
                    Swal.fire('Error!!', 'Please Check information!', 'error');
                    return;
                }
                console.log(data);
                $('#wallet-modal-confirm').addClass('hidden');
                $('#wallet-modal .modal-footer').addClass('hidden');
                $('#wallet-modal .modal-body').html('<p>Wallet Address - <strong>' + data.address + '</strong> </p>'
                    + '<p>Wallet private Key - <strong>' + data.private_key + '</strong> </p>');
            });
        }
    })

})
function nextStep(current_step) {
    $modal = $('#wallet-modal');
    modal_nextStep($modal, current_step);
    if (current_step == 1) {
        $modal.find('.left-nav-content').html(`
                        <div class="step-title">지갑 생성</div>
                        <hr>
                        <div class="modal-step">         
                            <span class="sign-span current">1</span>
                            <span class="sign-span">2</span>
                            <span class="sign-span">3</span>
                            <span class="sign-span">4</span>
                        </div>
                        <hr>
                        <div class="modal-step-content text-left">
                            <div>
                                지갑을 생성합니다.
                            </div>
                        </div>
                `);
        $modal.find('.right-content').html(`
                        <div class="content-head">Create Wallet!</div>
                        <hr>
                        <div class="content-body">ICON 지갑을 생성합니다</div>
                        <hr>
                        <div class="content-btn float-right">
                            <button id="nextStepCreateWallet" class="btn bg-seagreen" onclick="nextStep(2)">Next</button>
                        </div>
                `);
    } else if (current_step == 2) {
        $modal.find('.step-title').html(`정보입력`)
        $modal.find('.modal-step-content').html(`
                        <div class="text-left">
                            <p>비밀번호는 강력하고 본인이 확실하게 기억할 수 있는 비밀번호로 설정하세요.</p>
                            <p>비밀번호의 백업 및 관리는 전적으로 개인의 책임이며, 분실 시 어떤 방법으로도 복구될 수 없습니다.</p>
                        </div>
                `);
        $modal.find('.right-content').html(`
                        <div class="content-head">Wallet Infomation!</div>
                        <hr>
                        <div class="content-body">
                            <label> Wallet name</label>
                            <input type="text" id="wallet-name" class="form-control"  placeholder="enter wallet name">                                
                            <div class="password-form">
                                <label> Wallet password </label>
                                <input type="password" id="wallet-password" class="form-control"  placeholder="enter wallet password">
                                <label> Wallet password check</label>
                                <input type="password" id="wallet-password-check" class="form-control"  placeholder="enter wallet password retry">
                            </div>
                        </div>
                        <hr>
                        <div class="content-btn float-right">
                            <button id="nextStepCreateWallet" class="btn bg-seagreen" onclick="create_wallet();">Next</button>
                        </div>
                `);
    } else if (current_step == 3) {
        $modal.find('.step-title').html(`KeyStore 파일 다운로드`)
        $modal.find('.modal-step-content').html(`
                        <div class="text-left">
                            <p>지갑 백업 파일은 개인 키를 암호화하여 저장한 파일이며, 사용을 위해서는 지정한 지갑 비밀번호를 입력해야 합니다.</p>                            
                        </div>
                        <ul>
                            <li>지갑이 삭제된 경우나 다른 PC 사용 시, 지갑 백업 파일을 이용하여 지갑을 실행할 수 있습니다.</li>
                            <li>지갑 백업 파일은 비밀번호만 알면 지갑을 실행할 수 있는 중요한 정보이므로, 다른 사람에게 노출되지 않도록 안전하게 보관해야 합니다.</li>
                            <li>안전한 저장 장소가 준비되지 않은 경우 지금 즉시 다운로드 하지 않아도 되며, 다음에 ‘지갑 백업’ 메뉴를 선택해 다운로드할 수 있습니다.</li>
                        </ul>
                `);
        $modal.find('.right-content').html(`
                        <div class="content-head">Download keyStore!</div>
                        <hr>
                        <div class="content-body">
                            <div>
                                <a href="/wallet/create/keystore" download>download keystore...</a>
                            </div>
                        </div>
                        <hr>
                        <div class="content-btn float-right">
                            <button id="nextStepCreateWallet" class="btn bg-seagreen" onclick="nextStep(4)">Next</button>
                        </div>
                `);
    } else if (current_step == 4) {
        $modal.find('.step-title').html(`개인키 저장`)
        $modal.find('.modal-step-content').html(`
                        <div class="text-left">
                            <p>개인 키는 지갑을 직접 실행할 수 있는 고유 정보입니다.</p>                            
                            <p>프린트하거나 적어 두고 보관할 수 있습니다.</p>
                        </div>
                        <ul>
                            <li>개인 키만 보유하면 지갑 실행 및 송금이 가능하니, 누구에게도 노출되지 않도록 각별한 관리가 필요합니다.</li>
                            <li>지금 즉시 복사 또는 프린트하지 않더라도 ‘지갑 백업’ 메뉴를 선택해 다시 진행할 수 있습니다.</li>
                        </ul>
                `);
        $modal.find('.right-content').html(`
                        <div class="content-head">Wallet Private Key</div>
                        <hr>
                        <div class="content-body">
                            <div class="private-key">Private KEY</div>
                            <input class="form-control private-key-input" type="password" readonly="readyonly">
                            </div>
                        <hr>
                        <div class="content-btn float-right">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        </div>
                `);
        post_fetch("/wallet/create/get/privateKey", '{}').then(data => {
                $modal.find('.right-content .private-key-input').val(data.private_key);
            });
    }
};
function modalERROR($modal, erroMsg='Please Check information!'){
    nextStep(1);
    $modal.modal('hide');
    Swal.fire('Error!!', erroMsg, 'error');
}

function emptyFormCheck($form){
    isEmpty = false;
    $form.find('input').each(function(){
        if($(this).val().replace(/ /gi, "") == '' || $(this).val().replace(/ /gi, "").length < 1){
            isEmpty = true;
            return
        }
    })
    return isEmpty;
}
function formPasswordCheck($form){
    if($('#wallet-password').val() == $('#wallet-password-check').val()){
        return true;
    }else{
        return false;
    }
}
function modal_nextStep($modal, step) {
    $nav = $modal.find('.left-nav');
    $nav.find('.modal-step').find('.sign-span').each(function () {
        $(this).removeClass('current');
    })
    $nav.find('.modal-step').find('.sign-span:nth-child(' + step + ')').addClass('current');
}
function create_wallet() {
    if(emptyFormCheck($('#wallet-name .right-content .content-body'))){
        modalERROR($('#wallet-modal'),'Wallet Infomation hasn\'t empty !')
        return;
    }else if(!formPasswordCheck($('#wallet-name .right-content .content-body'))){
        modalERROR($('#wallet-modal'),'Please Check password!')
        return;
    }
    wallet_name = $('#wallet-name').val();
    wallet_password = $('#wallet-password').val();
    post_fetch('/wallet/create/', '{"wallet_name":"' + wallet_name +'","wallet_password":"' + wallet_password + '"}').then(data => {
        if (data === "fail") {
            modalERROR($('#wallet-modal'))
            return;
        }else{
            nextStep(3);
        }
    });
}
function post_fetch(endpoint, params) {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    return fetch(endpoint, {
        method: "POST",
        body: JSON.stringify(params),
        credentials: 'include',
        headers: {
            'X-CSRFToken': csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            return response.json();
        })
        .catch(e => {
            console.log("Internal error!!");
            return 'fail';
        });
}