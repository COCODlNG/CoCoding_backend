// =====================================================================================================================
const C = 'c';
const JAVA = 'java';
const PYTHON = 'python';

const C_MODE = 'text/x-csrc';
const JAVA_MODE = 'text/x-java';
const PYTHON_MODE = 'python';

const C_TEMPLATE = `#include<stdio.h>

void main(){
    printf("hello C!");
}`;

const PYTHON_TEMPLATE = "print('hello python!')";

const JAVA_TEMPLATE = `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello java!");
    }
}`;

const LANG_MAP = {
    [C]: {
        template: C_TEMPLATE,
        mode: C_MODE,
        name: 'C'
    },
    [JAVA]: {
        template: JAVA_TEMPLATE,
        mode: JAVA_MODE,
        name: 'Java'
    },
    [PYTHON]: {
        template: PYTHON_TEMPLATE,
        mode: PYTHON_MODE,
        name: 'Python'
    }
}
// =====================================================================================================================
const DISCARD_USER = 'discard_user';
const ADD_USER = 'add_user';
const MAKE_CALL = 'make_call';
const MAKE_ANSWER = 'make_answer';
const CHAT_MESSAGE = 'chat_message';
const CHANGE_CODE = 'edit_code';
const CHANGE_CANDIDATE = 'change_candidate'
const GET_CODE = 'get_code';

const WEB_RTC_CONF = {
    iceServers: [

{url:'stun:stun01.sipphone.com'},
{url:'stun:stun.ekiga.net'},
{url:'stun:stun.fwdnet.net'},
{url:'stun:stun.ideasip.com'},
{url:'stun:stun.iptel.org'},
{url:'stun:stun.rixtelecom.se'},
{url:'stun:stun.schlund.de'},
{url:'stun:stun.l.google.com:19302'},
{url:'stun:stun1.l.google.com:19302'},
{url:'stun:stun2.l.google.com:19302'},
{url:'stun:stun3.l.google.com:19302'},
{url:'stun:stun4.l.google.com:19302'},
{url:'stun:stunserver.org'},
{url:'stun:stun.softjoys.com'},
{url:'stun:stun.voiparound.com'},
{url:'stun:stun.voipbuster.com'},
{url:'stun:stun.voipstunt.com'},
{url:'stun:stun.voxgratia.org'},
{url:'stun:stun.xten.com'},
{
	url: 'turn:numb.viagenie.ca',
	credential: 'muazkh',
	username: 'webrtc@live.com'
},
{
	url: 'turn:192.158.29.39:3478?transport=udp',
	credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
	username: '28224511:1379330808'
},
{
	url: 'turn:192.158.29.39:3478?transport=tcp',
	credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
	username: '28224511:1379330808'
}
    ]
}


const USER_MEDIA_CONF = {
    video: true,
    audio: true,
}
