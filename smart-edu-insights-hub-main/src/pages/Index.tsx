
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import LoginForm from "@/components/Auth/LoginForm";

const Index = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    // Check if user is already logged in
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const userData = JSON.parse(userDataString);
      if (userData.isLoggedIn) {
        navigate("/dashboard");
      }
    }
  }, [navigate]);
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md mx-auto text-center mb-6">
        <h1 className="text-3xl font-bold text-lms-primary">MIT Learning Management System</h1>
        <p className="text-gray-600 mt-2">Access your virtual classroom, assignments, and grades</p>
      </div>
      
      <LoginForm />
      
      <div className="mt-8 text-center text-sm text-gray-500">
        <p>© 2025 MIT LMS. All rights reserved.</p>
      </div>
    </div>
  );
};

export default Index;
