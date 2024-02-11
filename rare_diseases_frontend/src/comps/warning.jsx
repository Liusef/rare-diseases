import { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from '../common/Button.jsx';
import "../style.css"

function Warning() {

  const [modalShow, setModalShow] = useState(true);

  const handleClose = () => setModalShow(false);

  return (
    <Modal
      show={modalShow}
      onHide={handleClose}
      backdrop="static"
      keyboard={false}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header>
        <Modal.Title id="contained-modal-title-vcenter">
          DISCLAIMER
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>
          By continuing, you acknowledge that RareSight is NOT a replacement for diagnosis, nor should results be used in isolation.
          <br/>
          RareSight is designed to be a preliminary exploration tool that uses your symptom list to identify potentially relevant rare diseases, and should be used as such.
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={handleClose} text="I understand. I will use this responsibly."/>
      </Modal.Footer>
    </Modal>
  );
}

export default Warning