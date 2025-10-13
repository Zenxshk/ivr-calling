import React, { useState, useEffect } from 'react';
import { Calendar, Clock, Users, Euro, BookOpen, ExternalLink, X, MapPin } from 'lucide-react';

const API_URL = 'http://localhost:5000/api/data';

const CoursesPage = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_URL);
      const result = await response.json();
      
      if (result.status === 'success') {
        setCourses(result.data);
      } else {
        throw new Error(result.message || 'Failed to fetch courses');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    if (!price) return 'Price not specified';
    if (price === 'Medium') return 'Medium Price Range';
    return typeof price === 'string' ? price : `${price}€`;
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'published': return 'bg-green-100 text-green-800';
      case 'active': return 'bg-blue-100 text-blue-800';
      case 'upcoming': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading courses...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-2xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Courses</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchCourses}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">Course Catalog</h1>
            <p className="mt-2 text-gray-600">Discover our available programs and courses</p>
            <div className="mt-4 text-sm text-gray-500">
              {courses.length} {courses.length === 1 ? 'course' : 'courses'} available
            </div>
          </div>
        </div>
      </header>

      {/* Course Cards Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              course={course}
              onViewDetails={() => setSelectedCourse(course)}
              formatPrice={formatPrice}
              getStatusColor={getStatusColor}
            />
          ))}
        </div>

        {courses.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📚</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No courses found</h3>
            <p className="text-gray-600">There are currently no courses available.</p>
          </div>
        )}
      </div>

      {/* Course Details Modal */}
      {selectedCourse && (
        <CourseModal
          course={selectedCourse}
          onClose={() => setSelectedCourse(null)}
          formatPrice={formatPrice}
          getStatusColor={getStatusColor}
        />
      )}
    </div>
  );
};

// Course Card Component - Shows Basic Info
const CourseCard = ({ course, onViewDetails, formatPrice, getStatusColor }) => {
  return (
    <div 
      className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-all duration-300 cursor-pointer transform hover:-translate-y-1"
      onClick={onViewDetails}
    >
      {/* Course Image */}
      <div className="h-48 bg-gray-200 relative">
        {course.thumbnail_image_url ? (
          <img
            src={course.thumbnail_image_url}
            alt={course.course_name}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'flex';
            }}
          />
        ) : null}
        <div className={`w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 ${course.thumbnail_image_url ? 'hidden' : 'flex'}`}>
          <BookOpen className="h-12 w-12 text-blue-400" />
        </div>
        
        {/* Status Badge */}
        {course.status && (
          <span className={`absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(course.status)}`}>
            {course.status}
          </span>
        )}
      </div>

      {/* Course Basic Info */}
      <div className="p-5">
        <h3 className="text-lg font-semibold text-gray-900 mb-3 line-clamp-2">
          {course.course_name || 'Unnamed Course'}
        </h3>

        {/* Basic Information Grid */}
        <div className="space-y-2">
          {course.level && (
            <div className="flex items-center text-sm text-gray-600">
              <BookOpen className="h-4 w-4 mr-2 flex-shrink-0" />
              <span className="truncate">{course.level}</span>
            </div>
          )}

          {course.age_group && (
            <div className="flex items-center text-sm text-gray-600">
              <Users className="h-4 w-4 mr-2 flex-shrink-0" />
              <span className="truncate">{course.age_group}</span>
            </div>
          )}

          {course.duration_hours && (
            <div className="flex items-center text-sm text-gray-600">
              <Clock className="h-4 w-4 mr-2 flex-shrink-0" />
              <span>{course.duration_hours} hours</span>
            </div>
          )}

          {course.mode && (
            <div className="flex items-center text-sm text-gray-600">
              <MapPin className="h-4 w-4 mr-2 flex-shrink-0" />
              <span>{course.mode}</span>
            </div>
          )}

          {course.price_range && (
            <div className="flex items-center text-sm text-gray-600 mt-3 pt-3 border-t border-gray-100">
              <Euro className="h-4 w-4 mr-2 flex-shrink-0" />
              <span className="font-semibold text-green-600">
                {formatPrice(course.price_range)}
              </span>
            </div>
          )}
        </div>

        {/* View Details Button */}
        <button
          onClick={onViewDetails}
          className="w-full mt-4 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
        >
          View Details
        </button>
      </div>
    </div>
  );
};

// Course Modal Component - Shows All Details
const CourseModal = ({ course, onClose, formatPrice, getStatusColor }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Modal Header with Image */}
        <div className="relative">
          <div className="h-80 bg-gray-200">
            {course.thumbnail_image_url ? (
              <img
                src={course.thumbnail_image_url}
                alt={course.course_name}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }}
              />
            ) : null}
            <div className={`w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 ${course.thumbnail_image_url ? 'hidden' : 'flex'}`}>
              <BookOpen className="h-20 w-20 text-blue-400" />
            </div>
          </div>

          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>

          {/* Status Badge */}
          {course.status && (
            <span className={`absolute top-4 left-4 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(course.status)}`}>
              {course.status}
            </span>
          )}
        </div>

        {/* Modal Content */}
        <div className="p-8">
          {/* Course Title */}
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            {course.course_name || 'Unnamed Course'}
          </h2>

          {/* Two Column Layout for Details */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Left Column - Course Info */}
            <div className="space-y-6">
              <div className="bg-blue-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-4">Course Information</h3>
                <div className="space-y-4">
                  {course.level && (
                    <DetailItem icon={BookOpen} label="Level" value={course.level} />
                  )}
                  
                  {course.age_group && (
                    <DetailItem icon={Users} label="Age Group" value={course.age_group} />
                  )}
                  
                  {course.mode && (
                    <DetailItem icon={MapPin} label="Mode" value={course.mode} />
                  )}
                  
                  {course.teacher_name && (
                    <DetailItem icon="👨‍🏫" label="Instructor" value={course.teacher_name} />
                  )}
                </div>
              </div>

              {course.schedule_details && (
                <div className="bg-green-50 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-green-900 mb-3">Schedule</h3>
                  <p className="text-green-800">{course.schedule_details}</p>
                </div>
              )}
            </div>

            {/* Right Column - Timing & Pricing */}
            <div className="space-y-6">
              <div className="bg-orange-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-orange-900 mb-4">Duration & Dates</h3>
                <div className="space-y-4">
                  {course.duration_hours && (
                    <DetailItem icon={Clock} label="Total Hours" value={`${course.duration_hours} hours`} />
                  )}
                  
                  {course.start_date && (
                    <DetailItem icon={Calendar} label="Start Date" value={course.start_date} />
                  )}
                  
                  {course.end_date && (
                    <DetailItem icon={Calendar} label="End Date" value={course.end_date} />
                  )}
                </div>
              </div>

              <div className="bg-purple-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-purple-900 mb-4">Pricing & Materials</h3>
                <div className="space-y-4">
                  {course.price_range && (
                    <DetailItem 
                      icon={Euro} 
                      label="Price Range" 
                      value={formatPrice(course.price_range)} 
                      valueClassName="text-green-600 font-semibold text-xl"
                    />
                  )}
                  
                  {course.materials_included && (
                    <DetailItem 
                      icon="📦" 
                      label="Materials Included" 
                      value={course.materials_included === 'Yes' ? '✅ Yes, all materials included' : '❌ No'} 
                    />
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Course Description */}
          {course.description && (
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 border-b pb-2">Course Description</h3>
              <p className="text-gray-700 leading-relaxed text-lg">{course.description}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-6 border-t border-gray-200">
            <button
              onClick={onClose}
              className="flex-1 bg-gray-300 text-gray-700 py-4 px-6 rounded-lg hover:bg-gray-400 transition-colors font-semibold text-lg"
            >
              Close
            </button>
            <button className="flex-1 bg-blue-600 text-white py-4 px-6 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg">
              Request Information
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Detail Item Component
const DetailItem = ({ icon: Icon, label, value, valueClassName = "" }) => {
  return (
    <div className="flex items-start">
      <div className="flex-shrink-0 h-6 w-6 text-gray-600 mt-1 mr-4">
        {typeof Icon === 'string' ? (
          <span className="text-2xl">{Icon}</span>
        ) : (
          <Icon className="h-6 w-6" />
        )}
      </div>
      <div className="flex-1">
        <div className="text-sm font-medium text-gray-600 uppercase tracking-wide">{label}</div>
        <div className={`text-lg text-gray-900 mt-1 ${valueClassName}`}>{value}</div>
      </div>
    </div>
  );
};

export default CoursesPage;