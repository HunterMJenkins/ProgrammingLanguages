import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class X {

    public boolean insertPrIssue(String pr, String issue, String projName) {
        Connection con = DBUtil.getConnection(dbcon, user, pswd);
        int count = 0;
        try {
            Statement comandoSql = con.createStatement();
            String sql = "INSERT INTO pr_issue VALUES ('" + pr + "', '" + issue + "', '" + projName + "')";
            count = comandoSql.executeUpdate(sql);
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
        return count > 0;
    }
}
