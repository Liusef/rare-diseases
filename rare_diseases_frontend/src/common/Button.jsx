import React from 'react';
import styled from 'styled-components';

const StyledButton = styled.button`
  transition: .1s;
  display: flex;
  width: fit-content;
  padding: 10px 30px;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-radius: 2px;
  border: 2px solid #000;
  background: #FFF;
  box-shadow: 4px 4px 0px 0px black;
  color: black;

  &:hover {
    transform: translate(4px, 4px);
    transition: .1s;
    box-shadow: 0px 0px 0px 0px black;
    border: 2px solid #000;
  }

  &:active {
    background: black;
    color: white;
  }
`;

const Button = ({ text, onClick }) => {
  return (
    <StyledButton onClick={onClick}>{text}</StyledButton>
  );
};

export default Button;
