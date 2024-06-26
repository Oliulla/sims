import sqlite3
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import os


# Set the backend to Agg to avoid GUI-related warnings
plt.switch_backend("agg")


def get_data():
    # Connect to the SQLite database
    conn = sqlite3.connect("db.sqlite3")

    # Load data from the database into Pandas DataFrames
    students = pd.read_sql_query("SELECT * FROM base_student", conn)
    grades = pd.read_sql_query("SELECT * FROM base_grade", conn)
    accommodations = pd.read_sql_query("SELECT * FROM base_accommodation", conn)

    conn.close()

    return students, grades, accommodations


def perform_analysis():
    students, grades, accommodations = get_data()

    # i. Calculate the number of students and gender ratio for each major
    student_count = students.groupby("major").size().reset_index(name="student_count")
    gender_counts = students.groupby(["major", "gender"]).size().unstack(fill_value=0)

    # Ensure 'Other' category exists even if it's empty
    if "Other" not in gender_counts.columns:
        gender_counts["Other"] = 0

    # Calculate total students per major
    gender_counts["total"] = gender_counts.sum(axis=1)

    # Calculate ratios
    gender_counts["male_ratio"] = gender_counts["Male"] / gender_counts["total"]
    gender_counts["female_ratio"] = gender_counts["Female"] / gender_counts["total"]
    gender_counts["other_ratio"] = gender_counts["Other"] / gender_counts["total"]

    # Reset index to make it flat for easier use in visualization
    gender_ratio = gender_counts.reset_index()

    # ii. Analyze the comparison of results in different majors
    # Filter out non-numeric grades before calculating mean
    grades_numeric = grades[grades["grade"].str.isnumeric()]
    results_by_major = grades_numeric.merge(
        students[["id", "major"]], left_on="student_id", right_on="id"
    )
    average_scores = results_by_major.groupby("major")["grade"].mean().reset_index()

    # iii. Analyze the relationship between student age and test scores
    age_scores = grades_numeric.merge(
        students[["id", "age"]], left_on="student_id", right_on="id"
    )
    age_score_relation = age_scores.groupby("age")["grade"].mean().reset_index()

    # iv. Analyze the relationship between students' regional distribution and test scores
    regional_scores = grades_numeric.merge(
        students[["id", "region"]], left_on="student_id", right_on="id"
    )
    regional_score_relation = (
        regional_scores.groupby("region")["grade"].mean().reset_index()
    )

    # v. Other analysis: Most popular major
    most_popular_major = student_count.sort_values(
        by="student_count", ascending=False
    ).head(1)

    # vi. Enrollment in every year
    enrollment_per_year = (
        students.groupby("year_of_enrollment")
        .size()
        .reset_index(name="enrollment_count")
    )

    # vii. Most popular dorm for the students
    dorm_popularity = (
        accommodations.groupby("building_name")
        .size()
        .reset_index(name="student_count")
        .sort_values(by="student_count", ascending=False)
        .head(1)
    )

    # viii. Most A+ in which Major
    a_plus_grades = grades[grades["grade"] == "A+"]
    a_plus_by_major = (
        a_plus_grades.merge(
            students[["id", "major"]], left_on="student_id", right_on="id"
        )
        if not a_plus_grades.empty
        else pd.DataFrame()
    )
    most_a_plus_major = (
        a_plus_by_major.groupby("major")
        .size()
        .reset_index(name="a_plus_count")
        .sort_values(by="a_plus_count", ascending=False)
        .head(1)
    )

    analysis_results = {
        "student_count": student_count,
        "gender_ratio": gender_ratio,
        "average_scores": average_scores,
        "age_score_relation": age_score_relation,
        "regional_score_relation": regional_score_relation,
        "most_popular_major": most_popular_major,
        "enrollment_per_year": enrollment_per_year,
        "dorm_popularity": dorm_popularity,
        "most_a_plus_major": most_a_plus_major,
    }

    # Save analysis reports as images
    save_analysis_images(analysis_results)

    return analysis_results


def save_analysis_images(analysis_results):
    if not os.path.exists("static/images"):
        os.makedirs("static/images")

    # i. Number of Students and Gender Ratio for Each Major
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=analysis_results["student_count"], x="major", y="student_count", ax=ax
    )
    ax.set_title("Number of Students for Each Major")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/images/student_count.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=analysis_results["gender_ratio"],
        x="major",
        y="male_ratio",
        color="b",
        label="Male",
        ax=ax,
    )
    sns.barplot(
        data=analysis_results["gender_ratio"],
        x="major",
        y="female_ratio",
        color="r",
        label="Female",
        ax=ax,
        bottom=analysis_results["gender_ratio"]["male_ratio"],
    )
    sns.barplot(
        data=analysis_results["gender_ratio"],
        x="major",
        y="other_ratio",
        color="g",
        label="Other",
        ax=ax,
        bottom=analysis_results["gender_ratio"]["male_ratio"]
        + analysis_results["gender_ratio"]["female_ratio"],
    )
    ax.set_title("Gender Ratio for Each Major")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/images/gender_ratio.png")
    plt.close()

    # ii. Comparison of Results in Different Majors
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=analysis_results["average_scores"], x="major", y="grade", ax=ax)
    ax.set_title("Average Scores in Different Majors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/images/average_scores.png")
    plt.close()

    # iii. Relationship Between Student Age and Test Scores
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=analysis_results["age_score_relation"], x="age", y="grade", ax=ax)
    ax.set_title("Relationship Between Student Age and Test Scores")
    plt.tight_layout()
    plt.savefig("static/images/age_score_relation.png")
    plt.close()

    # iv. Relationship Between Students' Regional Distribution and Test Scores
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=analysis_results["regional_score_relation"], x="region", y="grade", ax=ax
    )
    ax.set_title("Relationship Between Regional Distribution and Test Scores")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/images/regional_score_relation.png")
    plt.close()

    # v. Most Popular Major
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=analysis_results["most_popular_major"], x="major", y="student_count", ax=ax
    )
    ax.set_title("Most Popular Major")
    plt.tight_layout()
    plt.savefig("static/images/most_popular_major.png")
    plt.close()

    # vi. Enrollment in Every Year
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=analysis_results["enrollment_per_year"],
        x="year_of_enrollment",
        y="enrollment_count",
        ax=ax,
    )
    ax.set_title("Enrollment in Every Year")
    plt.tight_layout()
    plt.savefig("static/images/enrollment_per_year.png")
    plt.close()

    # vii. Most Popular Dorm for the Students
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=analysis_results["dorm_popularity"],
        x="building_name",
        y="student_count",
        ax=ax,
    )
    ax.set_title("Most Popular Dorm for the Students")
    plt.tight_layout()
    plt.savefig("static/images/dorm_popularity.png")
    plt.close()

    # viii. Most A+ in Which Major
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=analysis_results["most_a_plus_major"], x="major", y="a_plus_count", ax=ax
    )
    ax.set_title("Most A+ in Which Major")
    plt.tight_layout()
    plt.savefig("static/images/most_a_plus_major.png")
    plt.close()
