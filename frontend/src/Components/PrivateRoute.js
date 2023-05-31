import { useNavigate, useLocation } from "react-router-dom";

function PrivateRoute({ children }) {
  const isLoggedIn = !!localStorage.getItem("token"); // Replace this with your own authentication check logic
  const navigate = useNavigate();
  const location = useLocation();

  if (!isLoggedIn) {
    navigate('/login', { state: { from: location } });
    return null;
  }

  return children;
}


export default PrivateRoute;