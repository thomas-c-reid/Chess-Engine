import { FaLinkedin, FaInstagram, FaGithub } from 'react-icons/fa';
import './css/footer.css';
import ClosePanelIcon from './close_panel_icon';

const Footer = ({setIsFullScreen}) => {
    return (
        <div className="footer">
            <div className="footer-text-and-icons">      
            {/* social links */}
            <h1 className="footer-text">Thomas Reid - 2025</h1>
            <div className="social-icons">
                <a href="https://www.linkedin.com/in/thomas-reid-7298bb219/">
                    <FaLinkedin size={20} />
                </a>
                <a href="https://www.instagram.com/thomas_reid10/">
                    <FaInstagram size={20} />
                </a>
                <a href="https://github.com/thomas-c-reid" target="_blank" rel="noopener noreferrer">
                    <FaGithub size={20} />
                </a>
            </div>
            </div>
            <ClosePanelIcon setIsFullScreen={setIsFullScreen}></ClosePanelIcon>
        </div>
    );
}

export default Footer;