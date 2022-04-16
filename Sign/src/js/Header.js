import React from 'react'
import ReactDOM from 'react-dom';
import Modal from 'react-modal';

//import logo from '../../whiteLogo.png'



export default class Header extends React.Component {

    onModalPress() {
        var modal = document.getElementById("myModal");

        modal.style.display = "block";
    }

    onSpanPress() {
        var modal = document.getElementById("myModal");

        modal.style.display = "none";
    }

    render() {
        return(
            <div  id ='Header'>
                <img class='Logo' src='./blue.png'></img>
                <input id='setIcon' type='image' className='setIcon'src='./blue gear.png' onClick={this.onModalPress}></input>
                <div id="myModal" class="modal">
                    <div class="modal-content">
                        <span class="close" onClick={this.onSpanPress}>&times;</span>
                        <div class="setMenuHeader">
                            Settings
                        </div>
                        <div class='setContent'>
                            <div>Change Transcription Font Size:
                                <div class ='fontChange'>
                                    <button class="plus"> + </button>
                                    <>#</>
                                    <button class = 'minus'> - </button>
                                </div>
                            </div>
                            <div id='darkMode'>Enable Dark Mode: 
                                <div class='switch' id ='darkModeEnable'> 
                                    <input type="checkbox"/>
                                    <span class="slider round"></span>
                                </div>
                            </div>
                            <div class='voiceSelect'> Select Translation Voice:
                                <div class="dropdown">
                                    <button class="dropbtn">Select Voice</button>
                                    <div class="dropdown-content">
                                        <a href="#">Woman Voice</a>
                                        <a href="#">Man Voice</a>
                                        <a href="#">Gender Neutral Voice</a>
                                    </div>
                                </div>
                            </div>

                        </div>

                    </div>
                </div>
                <script type="text/javascript" scr='./modalFunctions.js'></script>
            </div>
        )
    }
}
