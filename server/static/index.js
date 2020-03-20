console.log('Running...');

const input_key = ' ';
let input_is_active = false;

const cmd_key = 'Control';
let cmd_is_down = false;

// window.onload = function () {

//     let inputModal = this.document.getElementById('inputModal');
//     inputModal.style.display = 'none';

//     let apply = function () {
//         if (input_is_active) {
//             inputModal.style.display = 'flex';
//             inputModal.children[0].focus();
//         } else {
//             inputModal.style.display = 'none';
//         }
//     }

//     window.onclick = (e) => {
//         console.log(e.target.className);
//         if (e.target.className === 'dimmer') {
//             input_is_active = false;
//         }
//         apply();
//     }

//     window.onkeydown = (e) => {
//         if (e.key === cmd_key) {
//             cmd_is_down = true;
//         }
//         if (e.key === input_key && cmd_is_down) {
//             input_is_active = true;
//         }
//         console.log(e.key)
//         if (e.key === 'Escape') {
//             input_is_active = false;
//         }
//     };
//     window.onkeyup = (e) => {
//         if (e.key === cmd_key) {
//             cmd_is_down = false;
//         }
//         apply();
//     };

// };
